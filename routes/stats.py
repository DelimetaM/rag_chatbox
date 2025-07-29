from fastapi import APIRouter
import json
import os

router = APIRouter()

# Vendos rrugën e saktë absolute për feedback_data.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
feedback_path = os.path.join(BASE_DIR, "data", "feedback_data.json")

@router.get("/stats")
def get_feedback_stats():
    try:
        if not os.path.exists(feedback_path):
            return {"message": "No feedback data found.", "average_rating": None, "total_feedbacks": 0}

        with open(feedback_path, "r", encoding="utf-8") as f:
            feedback_data = json.load(f)

        if not feedback_data:
            return {"message": "Feedback file is empty.", "average_rating": None, "total_feedbacks": 0}

        ratings = [entry["rating"] for entry in feedback_data if "rating" in entry]
        average_rating = sum(ratings) / len(ratings) if ratings else None
        total_feedbacks = len(ratings)

        return {
            "average_rating": average_rating,
            "total_feedbacks": total_feedbacks
        }
    except Exception as e:
        return {"error": str(e)}