from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: int

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    source_question: str