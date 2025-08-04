from fastapi import APIRouter, Depends
import sqlite3
import os
from app.auth.auth import get_current_user, admin_required

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "feedback.db")

router = APIRouter()

@router.get("/analytics/general", tags=["Analytics"])
def get_general_analytics(user: dict = Depends(admin_required)):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Numri total i user-ave
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    # Numri total i pyetjeve (chat_history)
    cursor.execute("SELECT COUNT(*) FROM chat_history")
    total_questions = cursor.fetchone()[0]

    # Numri total i feedback-eve
    cursor.execute("SELECT COUNT(*) FROM feedback")
    total_feedback = cursor.fetchone()[0]

    # Mesatarja e rating-ut
    cursor.execute("SELECT AVG(rating) FROM feedback")
    avg_rating = cursor.fetchone()[0] or 0

    # Top 3 pyetjet më të bëra
    cursor.execute("""
        SELECT question, COUNT(*) as count 
        FROM chat_history 
        GROUP BY question 
        ORDER BY count DESC 
        LIMIT 3
    """)
    top_questions = cursor.fetchall()

    conn.close()
    return {
        "total_users": total_users,
        "total_questions": total_questions,
        "total_feedback": total_feedback,
        "avg_rating": avg_rating,
        "top_questions": [
            {"question": q, "count": c} for q, c in top_questions
        ]
    }

@router.get("/analytics/user", tags=["Analytics"])
def get_user_analytics(user: dict = Depends(get_current_user)):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    username = user["username"]

    cursor.execute("SELECT COUNT(*) FROM chat_history WHERE username = ?", (username,))
    my_questions = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(rating) FROM feedback WHERE username = ?", (username,))
    my_avg_rating = cursor.fetchone()[0] or 0

    conn.close()
    return {
        "username": username,
        "questions_asked": my_questions,
        "avg_rating": my_avg_rating
    }
