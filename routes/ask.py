from fastapi import APIRouter
from models.request_models import AskRequest, AskResponse
from services.retrieval import retrieve_relevant_docs
from routes.memory.chat_memory import ChatMemory

chat_memory = ChatMemory()
router = APIRouter()

@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    # Marrim përgjigjen aktuale nga retrieval
    result = retrieve_relevant_docs(request.question)

    # Ruajmë në memorien vektoriale pyetjen dhe përgjigjen
    chat_memory.save_question_answer(request.question, result["answer"])

    # Marrim pyetjet e ngjashme nga memoria
    similar = chat_memory.search_similar_questions(request.question, top_k=3)

    # Kthejmë edhe related questions në response
    return AskResponse(
        answer=result["answer"],
        source_question=result["question"],
        related_questions=similar
    )

# Shfaq të gjithë historikun aktual të chat-it
@router.get("/chat-history")
def get_chat_history():
    return {"history": chat_memory.get_history()}

# Fshin të gjithë historikun e chat-it
@router.delete("/chat-history/clear")
def clear_chat_history():
    chat_memory.data.clear()
    return {"message": "Chat history cleared"}