from fastapi import APIRouter
from models.request_models import AskRequest
from services.retrieval import retrieve_relevant_docs

router = APIRouter()  # <- kjo është thelbësore!

@router.post("/ask")
def ask_question(request: AskRequest):
    result = retrieve_relevant_docs(request.question)
    return {
        "answer": result["answer"],
        "source_question": result["question"]
    }