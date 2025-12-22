#!/usr/bin/env python

from corpus_handler import CorpusHandler

SPEC = {
    "index_name": "legalbenchrag_v4",
    "model_embedding": "qwen3-embedding-8b",
    "search_spec_legalbench_chunk_v2": {
        "main": {
            "semantic_fields": ["text"],
            "semantic_index": "embedding",
        },
    },
}

if __name__ == "__main__":
    index_name = SPEC["index_name"]
    class_name = next(key for key in SPEC.keys() if key.startswith("search_spec")).replace("search_spec_", "")

    corpus = CorpusHandler.create_handler(class_name, SPEC)
    corpus.create_collection(index_name, recreate=True)
    corpus.populate_collection(index_name)
