from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    final_answer: str
    agents_used: List[str]
    trace: List[str]
    confidence: float
