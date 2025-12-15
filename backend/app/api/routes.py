from fastapi import APIRouter
from app.models.schemas import QueryRequest, QueryResponse
from app.core.coordinator import Coordinator

router = APIRouter()
coordinator = Coordinator()

@router.post("/query", response_model=QueryResponse)
def query_system(request: QueryRequest):
    return coordinator.handle_query(request.question)

@router.get("/memory")
def get_memory():
    return coordinator.memory_agent.get_conversation_memory()
