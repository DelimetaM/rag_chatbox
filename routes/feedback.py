from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.auth.auth import get_current_user
from data.database import insert_feedback
from services.response_evaluation import compute_quality_score

router = APIRouter()

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: int  # Vetëm përdoruesi e jep

@router.post("/feedback/", tags=["Feedback"])
def submit_feedback(feedback: FeedbackRequest, current_user: dict = Depends(get_current_user)):
    # Llogarit quality_score automatikisht
    score = compute_quality_score(feedback.question, feedback.answer)

    # Ruaje në databazë
    insert_feedback(
        question=feedback.question,
        answer=feedback.answer,
        rating=feedback.rating,
        quality_score=score,
        username=current_user["username"]
    )

    return {
        "message": "Feedback saved successfully.",
        "submitted_by": current_user["username"],
        "auto_quality_score": score
    }