from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict

from .openai import ChatCompletionResponse


class ChunkMetadata(BaseModel):
    collection_id: str
    document_id: str
    document_name: str
    document_part: int
    internet_query: str | None = None

    model_config = ConfigDict(
        extra="allow",
    )


class Chunk(BaseModel):
    object: Literal["chunk"] = "chunk"
    id: str | None = None
    metadata: ChunkMetadata | None = None
    content: str


class Search(BaseModel):
    score: float
    chunk: Chunk


class RagContext(BaseModel):  # mfs
    strategy: str
    references: list[str]


class RagChatCompletionResponse(ChatCompletionResponse):
    # Allow to return sources used with the rag
    # --
    # mfs-api
    rag_context: Optional[list[RagContext]] = None
    # albert-api
    search_results: List[Search] = []
