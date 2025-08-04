from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import List
from app.auth.auth import get_current_user
from services.retrieval import retrieve_top_k_docs
from services.feedback_loop import compute_feedback_weights
from services.response_generation import generate_answer
from services.response_evaluation import compute_quality_score
from data.database import save_chat_history, get_chat_history_db
from app.limiter import limiter
from routes.memory.chat_memory_sqlite import get_user_chat_memory

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

    # 1. Krijo ose ngarko chat memory per këtë user nga SQLite
    chat_memory = get_user_chat_memory(username)

    # 2. Kërko pyetje të ngjashme nga chat memory për kontekst
    similar_history = chat_memory.search_similar_questions(payload.question, top_k=2)
    context = ""
    for item in similar_history:
        context += f"Pyetja më parë: {item['question']}\nPërgjigja më parë: {item['answer']}\n"

    # 3. Gjej dokumentet më të afërta (retrieval nga FAQ)
    docs = retrieve_top_k_docs(payload.question, top_k=5)
    if not docs:
        raise HTTPException(status_code=404, detail="No relevant documents found")

    doc_questions = [doc["question"] for doc in docs]
    weights = compute_feedback_weights(payload.question, docs)

    # 4. Bashko context-in e memory me pyetjen aktuale
    full_prompt = context + "Pyetja ime: " + payload.question

    # 5. Gjenero përgjigjen me kontekst
    answer = generate_answer(full_prompt, docs, weights)
    quality_score = compute_quality_score(payload.question, answer)

    # 6. Ruaj në databazë historikun e bisedës
    
    # 7. Ruaj në chat memory (FAISS per user-in)
    chat_memory.save_question_answer(payload.question, answer)

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
    chat_memory = get_user_chat_memory(username)
    chat_memory.clear_history()
    return {"message": "Chat history cleared."}
