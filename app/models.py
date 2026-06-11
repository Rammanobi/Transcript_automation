from pydantic import BaseModel
from typing import List

class Chunk(BaseModel):
    chunk_id: int
    content: str

class Phase1Output(BaseModel):
    transcript_length: int
    chunk_count: int
    chunks: List[Chunk]

class ActionItemCandidate(BaseModel):
    title: str
    description: str
    assignee: str = ""
    priority: str = ""
    due_context: str = ""
    chunk_id: int
    confidence: float

class ChunkResult(BaseModel):
    chunk_id: int
    items: List[ActionItemCandidate]

class Phase2Output(BaseModel):
    processed_chunks: int
    successful_chunks: int
    failed_chunks: int
    raw_results: List[ChunkResult]

class FinalActionItem(BaseModel):
    action_id: str
    title: str
    description: str
    assignee: str
    priority: str
    due_context: str
    confidence: float
    source_chunks: List[int]

class Phase3Output(BaseModel):
    transcript_id: str
    total_chunks: int
    total_raw_items: int
    final_action_items: int
    actions: List[FinalActionItem]
