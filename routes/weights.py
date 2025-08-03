from fastapi import APIRouter, Depends
from app.auth.auth import get_current_user
import json
import os

router = APIRouter(
    prefix="/weights",
    tags=["Weights"]
)

# ✅ Rruga per faq_data.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAQ_PATH = os.path.join(BASE_DIR, "data", "faq_data.json")

@router.get("/")
def get_weights(user: dict = Depends(get_current_user)):
    with open(FAQ_PATH, "r", encoding="utf-8") as f:
        faq_data = json.load(f)
    return [
        {
            "id": item.get("id"),
            "question": item.get("question"),
            "weight": item.get("weight", 0.0)
        }
        for item in faq_data
    ]