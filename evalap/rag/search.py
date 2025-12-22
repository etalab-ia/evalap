import logging
import os
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

from elasticsearch import Elasticsearch, helpers

from evalap.clients.llm import LlmClient
from evalap.utils import retry

logging.getLogger("elastic_transport.transport").setLevel(logging.WARNING)

# Elasticsearch
ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL", "http://localhost:9200")
ELASTICSEARCH_USER = os.environ.get("ELASTICSEARCH_USER", "elastic")
ELASTICSEARCH_PASSWORD = os.environ.get("ELASTICSEARCH_PASSWORD", "")
ELASTICSEARCH_CREDS = (ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD)
# Qdrant
QDRANT_HOST = os.environ.get("QDRANT_HOST", "localhost")
QDRANT_GRPC_PORT = os.environ.get("QDRANT_GRPC_PORT", "6334")
QDRANT_REST_PORT = os.environ.get("QDRANT_REST_PORT", "6333")
QDRANT_URL = f"http://{QDRANT_HOST}:{QDRANT_REST_PORT}"
QDRANT_USE_GRPC = True


@dataclass
class SearchEngineConfig:
    default_engine: str = "elasticsearch"
    activate_hybrid: bool = True
    es_url: str = ELASTICSEARCH_URL
    es_creds: str = ELASTICSEARCH_CREDS
    qdrant_url: str = QDRANT_URL
    qdrant_grpc_port: int = QDRANT_GRPC_PORT
    qdrant_rest_port: int = QDRANT_REST_PORT
    qdrant_use_grpc: bool = QDRANT_USE_GRPC


@dataclass
class SearchEngineFilter:
    must: dict[str, str | list[str]] | None = None
    must_not: dict[str, str | list[str]] | None = None

    def to_must_es(self) -> list:
        must = []
        if not self.must:
            return must

        for k, v in self.must.items():
            if isinstance(v, (str, bool)):
                must.append({"term": {f"{k}": v}})
            elif isinstance(v, Iterable):
                must.append({"terms": {f"{k}": v}})
            else:
                raise TypeError(f"Filter value unknown: ({k} : {v})")

        return must

    def to_mustnot_es(self) -> list:
        must_not = []
        if not self.must_not:
            return must_not

        for k, v in self.must_not.items():
            if isinstance(v, (str, bool)):
                must_not.append({"term": {f"{k}": v}})
            elif isinstance(v, Iterable):
                must_not.append({"terms": {f"{k}": v}})
            else:
                raise TypeError(f"Filter value unknown: ({k} : {v})")

        return must_not


class SearchEngineClient:
    _embedding_fields = ["embedding", "embedding__secondary", "embedding__pack"]

    def __init__(self, **config):
        self.config = SearchEngineConfig(**config)

    @property
    def url(self):
        if self.config.default_engine == "elasticsearch":
            return self.config.es_url
        elif self.config.default_engine == "qdrant":
            return self.config.qdrant_url

    def create_collection(self, index: str, ixconfig: dict | None = None, engine: str = None, recreate=False):
        # @TODO: document ixconfig type !
        # One config doc per engine...
        engine = engine if engine else self.config.default_engine
        if ixconfig:
            ixconfig = ixconfig.get(engine, {})
        else:
            ixconfig = {}

        if not ixconfig:
            logging.warning(f"No configuration found for engine: {engine} for index {index}")

        match engine:
            case "elasticsearch":
                client = Elasticsearch(self.config.es_url, basic_auth=self.config.es_creds)
                if recreate:
                    client.indices.delete(index=index, ignore_unavailable=True)
                client.indices.create(
                    index=index,
                    settings=ixconfig.get("settings"),
                    mappings=ixconfig.get("mappings"),
                )

            case "qdrant":
                raise NotImplementedError
            case _:
                raise ValueError("Engine not supported: %s" % engine)

    def add_doc(self, index: str, document: dict, engine=None):
        engine = engine if engine else self.config.default_engine
        document_id = None
        if "id" in document:
            document_id = document["id"]
        elif "_id" in document:
            document_id = document["_id"]

        match engine:
            case "elasticsearch":
                client = Elasticsearch(self.config.es_url, basic_auth=self.config.es_creds)
                client.index(index=index, id=document_id, document=document)
            case "qdrant":
                raise NotImplementedError
            case _:
                raise ValueError("Engine not supported: %s" % engine)

    def add_batch(self, index: str, batch_documents: list[dict], engine=None):
        engine = engine if engine else self.config.default_engine

        match engine:
            case "elasticsearch":
                client = Elasticsearch(self.config.es_url, basic_auth=self.config.es_creds)
                helpers.bulk(client, batch_documents, index=index)
            case "qdrant":
                raise NotImplementedError
            case _:
                raise ValueError("Engine not supported: %s" % engine)

    def get_doc(self, index: str, id: str, engine=None, full=False) -> dict:
        engine = engine if engine else self.config.default_engine

        match engine:
            case "elasticsearch":
                client = Elasticsearch(self.config.es_url, basic_auth=self.config.es_creds)
                excludes = None if full else self._embedding_fields
                doc = client.get(index=index, id=id, source_excludes=excludes)
                doc = doc["_source"]
            case "qdrant":
                raise NotImplementedError
            case _:
                raise ValueError("Engine not supported: %s" % engine)

        return doc

    def update_doc(self, index: str, id: str, payload: dict, engine=None):
        engine = engine if engine else self.config.default_engine

        match engine:
            case "elasticsearch":
                client = Elasticsearch(self.config.es_url, basic_auth=self.config.es_creds)
                client.update(index=index, id=id, body={"doc": payload})
            case "qdrant":
                raise NotImplementedError
            case _:
                raise ValueError("Engine not supported: %s" % engine)

    @retry(tries=2, delay=2)
    def search(
        self,
        collection: str,
        query: str,
        limit: int = 5,
        offset: int = 0,
        engine: str = None,
        filters: dict = None,
        vector: list = None,
        method: str = "hybrid",
        lexical_fields: list | None = None,
        **kwargs,
    ) -> list[dict]:
        """
        filters: see SearchEngineFilter
        """
        engine = engine if engine else self.config.default_engine

        match engine:
            case "elasticsearch":
                results = self._search_es(
                    collection,
                    query,
                    limit=limit,
                    offset=offset,
                    filters=filters,
                    vector=vector,
                    method=method,
                    **kwargs,
                )
            case "qdrant":
                results = self._search_qdrant(
                    collection,
                    query,
                    limit=limit,
                    offset=offset,
                    filters=filters,
                    vector=vector,
                    method=method,
                    **kwargs,
                )
            case _:
                raise ValueError("Index unknown: %s" % engine)

        return results

    def exists(self, collection: str, engine: str = None) -> bool:
        engine = engine if engine else self.config.default_engine

        match engine:
            case "elasticsearch":
                res = self._exists_es(collection)
            case "qdrant":
                raise NotImplementedError
            case _:
                raise ValueError("Index unknown: %s" % engine)

        return res

    def _rrf_ranker(
        self,
        group_results,
        limit: int,
        k: float = 10,
        lexical_weight: float = 1,
        semantic_weight: float = 1.5,
        **kwargs,
    ):
        """
        Combine search results using Reciprocal Rank Fusion (RRF)
        :param group_results: A list of result lists from different searches
        :param k: The constant k in the RRF formula
        :return: A combined list of results with updated scores
        """
        combined_scores = {}
        doc_map = {}
        weights = {  # order matter !
            "lexical": lexical_weight,
            "semantic": semantic_weight,
        }
        for search_type, results in zip(weights.keys(), group_results):
            for rank, result in enumerate(results):
                doc_id = result["_id"]
                if doc_id not in combined_scores:
                    combined_scores[doc_id] = 0
                    doc_map[doc_id] = result
                combined_scores[doc_id] += weights[search_type] / (k + rank + 1)

        # Sort combined results by their RRF scores in descending order
        ranked_results = sorted(combined_scores.items(), key=lambda item: item[1], reverse=True)

        reranked_results = []
        for doc_id, rrf_score in ranked_results:
            document = doc_map[doc_id]
            document["_rrf_score"] = rrf_score
            reranked_results.append(document)

        return reranked_results[:limit]

    #
    # Elasticsearch related methods
    #
    def _exists_es(self, collection: str) -> bool:
        client = Elasticsearch(self.config.es_url, basic_auth=self.config.es_creds)
        return bool(client.indices.exists(index=collection))

    def _search_es(
        self,
        collection: str,
        query: str,
        limit: int,
        offset: int = 0,
        filters: dict | None = None,
        fuzzy_search: bool = False,
        expansion_factor: float = 4,
        vector: list = None,
        method: str = "hybrid",
        lexical_fields: list | None = None,
        boost_lexical_fields: dict | None = None,
        model_embedding: str | None = None,
        **kwargs,
    ) -> list[dict]:
        index = collection
        # No ranking filters
        filters = filters if filters else {}
        filters = SearchEngineFilter(**(filters or {}))

        # Lexical search
        # --
        fuzziness = {}
        if fuzzy_search and len(query.split()) < 25:
            fuzziness = {"fuzziness": "AUTO"}
        should = []
        if lexical_fields is None:
            lexical_fields = ["*"]

        # Handle boost_query
        if kwargs.get("boost_query"):
            boosted_query = [f"{term}^{2}" for i, term in enumerate(kwargs["boost_query"].split())]
            should.append(
                {
                    "query_string": {
                        "query": " ".join(boosted_query),
                        "fields": lexical_fields,
                    }
                }
            )

        # Handle boost_lexical_fields
        if boost_lexical_fields:
            for field, boost_value in boost_lexical_fields.items():
                should.append(
                    {
                        "multi_match": {
                            "query": query,
                            "type": "most_fields",
                            "fields": [field],
                            "boost": boost_value,
                            **fuzziness,
                        }
                    }
                )

        lexical_query = {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": query,
                            "type": "most_fields",
                            "fields": lexical_fields,
                            **fuzziness,
                        }
                    }
                ],
                "should": should,
                "filter": filters.to_must_es(),
                "must_not": filters.to_mustnot_es(),
            }
        }

        # Semantic search
        llm_client = LlmClient()
        embedding_field = "embedding"
        if vector is None and method != "lexical":
            vector = llm_client.create_embeddings(query, model=model_embedding)
        elif isinstance(vector, dict):
            embedding_field, vector = next(iter(vector.items()))
            if len(vector) > 1:
                logging.warning("Multiple vector search is not implemented.")

        K = int(limit * expansion_factor)
        semantic_query = {
            "field": embedding_field,
            "query_vector": vector,
            "k": K,
            "num_candidates": max(K * 10, 100),
            "filter": {"bool": {"must": filters.to_must_es(), "must_not": filters.to_mustnot_es()}},
        }

        if method == "semantic" or not query:
            lexical_query = {}
        if method == "lexical":
            semantic_query = {}

        hits = self._hybrid_search_es(
            index, lexical_query, semantic_query, limit, expansion_factor, offset, **kwargs
        )

        return hits

    def _hybrid_search_es(
        self,
        index,
        lexical_query,
        semantic_query,
        limit: int,
        expansion_factor: float,
        offset: int = 0,
        **kwargs,
    ):
        # RRF is not available in the free license.
        # body = {
        #    "query": lexical_query,
        #    "knn": semantic_query,
        #     "rank": {"rrf": {}},
        #    "size": limit,
        #    "_source": {"excludes": self._embedding_fields},
        # }
        # res = client.search(index=index, body=body)
        # hits = [x.get("_source") for x in res["hits"]["hits"] if x]
        # --
        # See also: https://elasticsearch-py.readthedocs.io/en/v8.14.0/async.html
        lexical_results = []
        semantic_results = []
        with ThreadPoolExecutor(max_workers=2) as executor:
            lexical_query_body = {
                "query": lexical_query,
                "size": int(limit * expansion_factor),
                "from": offset,
                "_source": {"excludes": self._embedding_fields},
            }
            semantic_query_body = {
                "knn": semantic_query,
                "size": int(limit * expansion_factor),
                "from": offset,
                "_source": {"excludes": self._embedding_fields},
            }

            if lexical_query:
                lexical_future = executor.submit(self._search_lowlevel_es, index, lexical_query_body)
                lexical_results = [x for x in lexical_future.result()["hits"]["hits"] if x]

            if semantic_query:
                semantic_future = executor.submit(self._search_lowlevel_es, index, semantic_query_body)
                semantic_results = [x for x in semantic_future.result()["hits"]["hits"] if x]

        results = self._rrf_ranker([lexical_results, semantic_results], limit=limit, **kwargs)
        hits = [(x.get("_source", {}) | {"__score": x["_score"]}) for x in results]
        return hits

    def _search_lowlevel_es(self, index, query):
        client = Elasticsearch(self.config.es_url, basic_auth=self.config.es_creds)
        return client.search(index=index, body=query)

    #
    # Qdrant related methods
    #

    def _search_qdrant(self, collection: str, query: str, limit: int, offset: int = 0, **kwargs) -> list[dict]:
        raise NotImplementedError
