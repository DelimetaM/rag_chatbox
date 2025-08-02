from fastapi import APIRouter, Depends
from models.request_models import AskRequest, AskResponse
from services.retrieval import retrieve_relevant_docs, faq_data, embed_text, cosine_similarity
from routes.memory.chat_memory import ChatMemory
from app.auth.auth import get_current_user
from services.feedback_loop import compute_feedback_weights
from services.response_evaluation import compute_quality_score

chat_memory = ChatMemory()
router = APIRouter()

@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest, user: dict = Depends(get_current_user)):
    all_docs = faq_data
    weights = compute_feedback_weights(request.question, all_docs)

    query_embedding = embed_text(request.question)

    best_score = -1
    best_doc = None

    for i, doc in enumerate(all_docs):
        doc_embedding = embed_text(doc["question"])
        similarity = cosine_similarity(query_embedding, doc_embedding)

        weight = weights[i]
        final_score = similarity * (1 + weight)  # kombinim i peshës + ngjashmëri

        if final_score > best_score:
            best_score = final_score
            best_doc = doc

    result = best_doc if best_doc else retrieve_relevant_docs(request.question)

    # Ruaj në memory chat
    chat_memory.save_question_answer(request.question, result["answer"])

    # ✅ Gjej pyetjet e ngjashme vetëm nëse përdoruesi e kërkon
    if request.show_related:
        similar = chat_memory.search_similar_questions(request.question, top_k=3)
    else:
        similar = []

    # Llogarisim cilësinë e përgjigjes me keyword overlap
    score = compute_quality_score(request.question, result["answer"])

    return AskResponse(
        answer=result["answer"],
        source_question=result["question"],
        related_questions=similar,
        quality_score=score
    )

@router.get("/chat-history")
def get_chat_history(user: dict = Depends(get_current_user)):
    return {"history": chat_memory.get_history()}

@router.delete("/chat-history/clear")
def clear_chat_history(user: dict = Depends(get_current_user)):
    chat_memory.clear_history()
    return {"message": "Chat history cleared"}