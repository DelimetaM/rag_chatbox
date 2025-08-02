from pydantic import BaseModel, Field
from typing import List, Optional

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: int = Field(..., ge=1, le=10)

class AskRequest(BaseModel):
    question: str
    show_related: bool = True  # ✅ kontroll nëse do të shfaqen pyetjet e lidhura

class AskResponse(BaseModel):
    answer: str
    source_question: str
    related_questions: Optional[List[dict]] = None  # ✅ lista e pyetjeve të mëparshme (nëse kërkohet)
    quality_score: Optional[float] = None  # ✅ vlerësimi automatik i përgjigjes