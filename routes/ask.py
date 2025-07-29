from fastapi import APIRouter
from models.request_models import AskRequest, AskResponse
from services.retrieval import retrieve_relevant_docs

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    result = retrieve_relevant_docs(request.question)

    return AskResponse(
        answer=result["answer"],
        source_question=result["question"]
    )