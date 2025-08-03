import re
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, validator, constr

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

class RegisterUserRequest(BaseModel):
    username: constr(strip_whitespace=True, min_length=3, max_length=20)  # type: ignore
    email: EmailStr
    country: Optional[str] = None
    password: constr(min_length=8, max_length=64)  # type: ignore

    @validator("username")
    def username_format(cls, v):
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username mund të përmbajë vetëm shkronja, numra dhe '_'")
        return v

    @validator("password")
    def strong_password(cls, v):
        if (not re.search(r"[A-Z]", v)
            or not re.search(r"[a-z]", v)
            or not re.search(r"\d", v)
            or not re.search(r"[!@#$%^&*]", v)):
            raise ValueError("Password duhet të ketë të paktën 1 shkronjë të madhe, 1 të vogël, 1 numër dhe 1 simbol (!@#$%^&*)")
        return v

    @validator("email")
    def email_domain_check(cls, v):
        if v.endswith("@tempmail.com"):
            raise ValueError("Nuk lejohen emaile temporare (tempmail.com)")
        return v
