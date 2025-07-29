from fastapi import APIRouter
from models.request_models import FeedbackRequest
from data.database import insert_feedback

router = APIRouter()

@router.post("/feedback")
def submit_feedback(feedback: FeedbackRequest):
    insert_feedback(feedback.question, feedback.answer, feedback.rating)
    return {"message": "Feedback submitted successfully"}