from enum import Enum
from typing import Any, Dict, List, Literal

from pydantic import BaseModel

from .openai import ChatCompletionResponse


class SearchMethod(str, Enum):
    """Enum representing the search methods available (will be displayed in this order in playground)."""

    MULTIAGENT = "multiagent"
    HYBRID = "hybrid"
    SEMANTIC = "semantic"
    LEXICAL = "lexical"


class Chunk(BaseModel):
    object: Literal["chunk"] = "chunk"
    id: int
    metadata: Dict[str, Any]
    content: str


class Search(BaseModel):
    method: SearchMethod
    score: float
    chunk: Chunk


class RagChatCompletionResponse(ChatCompletionResponse):
    # Get the references for RAG usage
    # --
    # albert-api
    search_results: List[Search] = []
