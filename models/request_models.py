from pydantic import BaseModel, Field
from typing import List, Optional

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: int = Field(..., ge=1, le=10) 

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    source_question: str
    related_questions: Optional[List[dict]] = None