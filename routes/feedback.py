from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from data.database import insert_feedback
from app.auth.auth import get_current_user
from routes.memory.chat_memory import memory  
from app.limiter import limiter

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"]
)

def normalize_text(text: str) -> str:
    """
    Normalize text by stripping extra whitespace, lowercasing
    and collapsing multiple spaces into one.
    """
    return " ".join(text.strip().lower().split())

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: int

@router.post("", summary="Submit feedback")
@limiter.limit("5/minute")  # Rate limiting: 5 kërkesa në min
def submit_feedback(
    feedback: FeedbackRequest,
    request: Request,                
    user=Depends(get_current_user)
):
    username = user["username"]

    try:
        insert_feedback(
            question=feedback.question,
            answer=feedback.answer,
            rating=feedback.rating,
            username=username
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Feedback stored successfully"}
