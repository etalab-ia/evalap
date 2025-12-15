import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generator, Sequence

from corpus_loader import load_legalbenchrag
from search import SearchEngineClient
from tqdm import tqdm

from evalap.clients import LlmClient
from evalap.logger import logger

BATCH_EMBEDDING_SIZE = 32


def embed(data: None | str | list[str], spec: dict) -> None | list:
    if data is None:
        return None

    model = spec["model_embedding"]
    client = LlmClient()
    if isinstance(data, list):
        # Keep track of None positions
        indices_of_none = [i for i, x in enumerate(data) if x is None]
        filtered_data = [x for x in data if x is not None]
        if not filtered_data:
            return [None] * len(data)

        # Apply the original function on filtered data
        try:
            embeddings = client.create_embeddings(filtered_data, model=model)
        except Exception as err:
            print(filtered_data)
            raise err

        # Reinsert None at their original positions in reverse order
        for index in reversed(indices_of_none):
            embeddings.insert(index, None)

        return embeddings

    # Fall back to single data input
    return client.create_embeddings(data, model=model)


class CorpusHandler(ABC):
    _type = "not implemented"
    id_attribute = "not implemented"

    def __init__(self, spec: dict, **corpus_params):
        self._spec = spec
        self._corpus_params = corpus_params

        # Load in implemented classes
        self._corpus: list[dict] | None = None
        self._corpus_meta: dict | None = None

    def __repr__(self):
        return f"`{self._type} corpus (n_doc: {len(self._corpus or [])})`"

    def load_index_config(self, placeholders: dict) -> dict:
        filename = f"{self._type}.index.json"
        path = Path(__file__).resolve().parent / filename
        if not path.exists():
            return {}

        with open(path) as file:
            config = json.load(file)

        # Render placeholder
        for k, v in placeholders.items():
            placeholder = "__" + k.upper() + "__"
            # Check if value is of type int, str, or bool and replace the placeholder with the appropriate JSON formatting
            if isinstance(v, str):
                value = json.dumps(v)
            elif isinstance(v, int):
                value = str(v)
            elif isinstance(v, bool):
                value = "true" if v else "false"
            json_string = json.dumps(config).replace(f'"{placeholder}"', value)
            config = json.loads(json_string)

        return config

    @classmethod
    def create_handler(cls, corpus_type: str, spec: dict, **corpus_params) -> "CorpusHandler":
        """Get the appropriate handler subclass from the string corpus name."""
        for handler in CORPUSES_HANDLERS:
            if corpus_type == handler._type:
                return handler(spec, **corpus_params)
        raise ValueError(f"Corpus '{corpus_type}' is not recognized")

    def create_collection(self, index: str, recreate: bool = False):
        probe_vector = embed("Hey, I'am a probe", self._spec)
        ixconfig = self.load_index_config({"embedding_size": len(probe_vector)})
        se_client = SearchEngineClient()
        se_client.create_collection(index, ixconfig, recreate=recreate)

    def populate_collection(self, index, batch_size: int = BATCH_EMBEDDING_SIZE, **load_params):
        self.load(**load_params)
        se_client = SearchEngineClient()
        logger.info(f"indexing {self} in index {index} to {se_client.url}")
        for batch_documents, batch_embeddings in self.iter_docs_embeddings(batch_size):
            for doc, embeddings in zip(batch_documents, batch_embeddings):
                doc["_id"] = doc[self.id_attribute]
                if embeddings is not None:
                    # Handle multiple embeddings
                    for embedding_index, embedding in embeddings.items():
                        doc[embedding_index] = embedding

            try:
                se_client.add_batch(index, batch_documents)
            except Exception as e:
                print(f"failed for batch (size {len(batch_documents)}) ({e}):")
                print("Adding document for this batch individually...")
                for b in batch_documents:
                    try:
                        se_client.add_batch(index, [b])
                    except Exception as e:
                        b.pop("embedding")
                        print("The following document failed to be indexed")
                        print(b)
                        for error in e.errors:
                            print(json.dumps(error, indent=2))
                        raise e

    def iter_docs_embeddings(self, batch_size: int) -> Generator[tuple[list, list], None, None]:
        """Return a batch tuple of
        1. the batched items
        2. the batch embeddings: One entry is a dict of the embedding (list[float]) per index_name
        """
        desc = f"Processing corpus {self} with embeddings..."

        # Embedding specification
        search_spec = self._spec.get(f"search_spec_{self._type}")
        K = 0
        if search_spec:
            eb_indexes = [x["semantic_index"] for x in search_spec.values() if x.get("semantic_index")]
            eb_fields = [x["semantic_fields"] for x in search_spec.values() if x.get("semantic_fields")]
            K = len(eb_indexes)
            assert len(eb_indexes) == len(eb_fields)

        if K == 0:
            logger.warning(f"No embeddings spec for {self}")

        for batch in self.iter_docs(batch_size=batch_size, desc=desc):
            if K == 0:
                # No embeddings...
                yield batch, [None] * len(batch)
                continue

            batch_embeddings = embed(
                [self.doc_to_chunk(x, fields) for fields in eb_fields for x in batch],
                self._spec,
            )

            # dezipped_embeddings
            batch_embeddings = [
                {index_name: embedding for index_name, embedding in zip(eb_indexes, embeddings)}
                for embeddings in [batch_embeddings[i : i + K] for i in range(0, len(batch_embeddings), K)]
            ]

            assert len(batch) == len(batch_embeddings)
            yield batch, batch_embeddings

    def iter_docs(self, batch_size: int, desc: str = None) -> Generator[list, None, None]:
        if not desc:
            desc = f"Processing corpus: {self}..."

        corpus = self._corpus
        num_chunks = len(corpus) // batch_size
        if len(corpus) % batch_size != 0:
            num_chunks += 1

        for i in tqdm(range(num_chunks), desc=desc):
            start_idx = i * batch_size
            end_idx = min(start_idx + batch_size, len(corpus))
            yield corpus[start_idx:end_idx]

    #
    # Abstract method
    #

    @abstractmethod
    def doc_to_chunk(self, doc: dict, fields: Sequence | None = None) -> str:
        raise NotImplementedError("Subclasses should implement this!")

    @abstractmethod
    def load(self, **kwargs) -> list[dict]:
        raise NotImplementedError("Subclasses should implement this!")


class LegalBenchHandlerV1(CorpusHandler):
    _type = "legalbench_v1"
    id_attribute = "_id"

    def load(self, verbose=True, **kwargs) -> list[dict]:
        documents = load_legalbenchrag(max_words=300)

        if len(documents) == 0:
            logger.warning(f"No documents to add to the corpus '{self}'")

        self._corpus = documents
        return documents

    def doc_to_chunk(self, doc: dict, fields: Sequence | None = None) -> str | None:
        if not fields:
            return None

        texts = []
        for field in fields:
            if not doc.get(field):
                continue

            terms = doc[field]
            terms = terms.strip("., ")
            texts.append(terms)

        text = " - ".join(texts)
        return text


CORPUSES_HANDLERS = [LegalBenchHandlerV1]
