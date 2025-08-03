import sqlite3
import os
import json
from datetime import datetime
from services.response_evaluation import compute_quality_score

#Pathet(Rruget) absolute
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "feedback.db")
FAQ_PATH = os.path.join(BASE_DIR, "data", "faq_data.json")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #Tabela feedback
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            rating INTEGER NOT NULL,
            username TEXT,
            quality_score REAL DEFAULT 0
        )
    """)

    #Tabela users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT,
            country TEXT,
            password TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    #Tabela chat_history (ruan historikun e plotë të bisedës për çdo user)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

# Shto përdorues të ri
def create_user(username: str, email: str, country: str, password: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    cursor.execute(
        "INSERT INTO users (username, email, country, password, created_at) VALUES (?, ?, ?, ?, ?)",
        (username, email, country, password, created_at)
    )
    conn.commit()
    conn.close()

def user_exists(username: str, email: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

# Merr përdorues sipas username
def get_user_by_username(username: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "username": row[1], "password": row[2]}
    return None

# Shto feedback me quality_score dhe username
def insert_feedback(question, answer, rating, username=None):
    quality_score = compute_quality_score(question, answer)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO feedback (question, answer, rating, username, quality_score)
        VALUES (?, ?, ?, ?, ?)
    """, (question, answer, rating, username, quality_score))

    conn.commit()
    conn.close()

# ---------- CHAT HISTORY -----------

def save_chat_history(username: str, question: str, answer: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.utcnow().isoformat()
    cursor.execute(
        "INSERT INTO chat_history (username, question, answer, timestamp) VALUES (?, ?, ?, ?)",
        (username, question, answer, timestamp)
    )
    conn.commit()
    conn.close()

def get_chat_history_db(username: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT question, answer, timestamp FROM chat_history WHERE username = ? ORDER BY timestamp DESC",
        (username,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {"question": row[0], "answer": row[1], "timestamp": row[2]}
        for row in rows
    ]

def clear_chat_history_db(username: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM chat_history WHERE username = ?",
        (username,)
    )
    conn.commit()
    conn.close()