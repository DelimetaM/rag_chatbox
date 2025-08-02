from fastapi import APIRouter, Depends
from models.request_models import FeedbackRequest
from data.database import insert_feedback
from app.auth.auth import get_current_user
from services.response_evaluation import compute_quality_score  # ✅ Import i saktë

router = APIRouter()

@router.post("/feedback")
def submit_feedback(
    feedback: FeedbackRequest,
    user: dict = Depends(get_current_user)
):
    # ✅ Llogarit cilësinë e përgjigjes
    quality_score = compute_quality_score(feedback.question, feedback.answer)

    # ✅ Kalo të gjithë 4 parametrat
    insert_feedback(feedback.question, feedback.answer, feedback.rating, quality_score)

    return {"message": "Feedback submitted successfully"}