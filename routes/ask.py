from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import List
from app.auth.auth import get_current_user
from services.retrieval import retrieve_top_k_docs
from services.feedback_loop import compute_feedback_weights
from services.response_generation import generate_answer
from services.response_evaluation import compute_quality_score
from data.database import save_chat_history, get_chat_history_db, clear_chat_history_db
from app.limiter import limiter

router = APIRouter()

class AskRequest(BaseModel):
    question: str
    show_related: bool = False

class AskResponse(BaseModel):
    answer: str
    quality_score: float
    related_questions: List[str] 

@router.post("/ask", response_model=AskResponse, tags=["Q&A"])
@limiter.limit("5/minute")  # Rate limiting: 5 kërkesa në min
def ask_question(
    payload: AskRequest,
    request: Request,  
    user: dict = Depends(get_current_user)
):
    username = user["username"]

    # Gjej dokumentet më të afërta
    docs = retrieve_top_k_docs(payload.question, top_k=5)
    if not docs:
        raise HTTPException(status_code=404, detail="No relevant documents found")

    doc_questions = [doc["question"] for doc in docs]
    weights = compute_feedback_weights(payload.question, docs)
    answer = generate_answer(payload.question, docs, weights)
    quality_score = compute_quality_score(payload.question, answer)

    # Ruaj në databazë 
    save_chat_history(username, payload.question, answer)

    response = {
        "answer": answer,
        "quality_score": quality_score,
        "related_questions": doc_questions if payload.show_related else []
    }
    return response

@router.get("/chat-history", tags=["Chat History"])
def get_chat_history(user: dict = Depends(get_current_user)):
    username = user["username"]
    history = get_chat_history_db(username)
    return {"history": history}

@router.delete("/chat-history", tags=["Chat History"])
def clear_chat_history(user: dict = Depends(get_current_user)):
    username = user["username"]
    clear_chat_history_db(username)
    return {"message": "Chat history cleared."}
