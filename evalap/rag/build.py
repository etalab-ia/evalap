#!/usr/bin/env python

from corpus_handler import CorpusHandler

SPEC = {
    "model_embedding": "BAAI/bge-m3",
    "search_spec_legalbench_v1": {
        "main": {
            "lexical_fields": ["text"],
            "semantic_fields": ["text"],
            "semantic_index": "embedding",
            "semantic_weight": 1.5,
        },
    },
}

if __name__ == "__main__":
    index_name = "legalbenchrag_v1"
    corpus = CorpusHandler.create_handler("legalbench_v1", SPEC)
    corpus.create_collection(index_name, recreate=True)
    corpus.populate_collection(index_name)
