import os
import sqlite3
from fastapi import APIRouter

router = APIRouter()

# Vendos rrugën absolute të databazës
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "feedback.db")

@router.get("/stats")
def get_feedback_stats():
    try:
        if not os.path.exists(DB_PATH):
            return {"message": "Database not found.", "average_rating": None, "total_feedbacks": 0}

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT rating FROM feedback")
        ratings = [row[0] for row in cursor.fetchall()]
        conn.close()

        if not ratings:
            return {"message": "No feedback data found.", "average_rating": None, "total_feedbacks": 0}

        average_rating = sum(ratings) / len(ratings)
        total_feedbacks = len(ratings)

        return {
            "average_rating": average_rating,
            "total_feedbacks": total_feedbacks
        }

    except Exception as e:
        return {"error": str(e)}