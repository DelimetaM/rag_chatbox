from fastapi import APIRouter, Depends
from app.auth.auth import admin_required
import json
import os

router = APIRouter(
    prefix="/weights",
    tags=["Weights"]
)

# Rruga per faq_data.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAQ_PATH = os.path.join(BASE_DIR, "data", "faq_data.json")

@router.get("/", dependencies=[Depends(admin_required)])
def get_weights():
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
