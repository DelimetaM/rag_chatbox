from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: int = Field(..., ge=1, le=10)

class AskRequest(BaseModel):
    question: str
    show_related: bool = True

class AskResponse(BaseModel):
    answer: str
    source_question: str
    related_questions: Optional[List[dict]] = None
    quality_score: Optional[float] = None

# ✅ Model për regjistrimin e përdoruesit
class RegisterUserRequest(BaseModel):
    username: str
    email: EmailStr
    country: Optional[str] = None
    password: str