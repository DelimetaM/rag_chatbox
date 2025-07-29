from pydantic import BaseModel

class AskRequest(BaseModel):
    question: str

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: int