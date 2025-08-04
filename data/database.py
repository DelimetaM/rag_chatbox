import sqlite3
import os
from datetime import datetime
from services.response_evaluation import compute_quality_score

# HASH password
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str):
    return pwd_context.hash(password)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "feedback.db")
FAQ_PATH = os.path.join(BASE_DIR, "data", "faq_data.json")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabela feedback (tani me koment)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            rating INTEGER NOT NULL,
            username TEXT,
            quality_score REAL DEFAULT 0,
            comment TEXT         -- SHTO KOLUMNEN COMMENT!
        )
    """)

    # Shto kolonën 'comment' nëse mungon (safe ALTER)
    cursor.execute("PRAGMA table_info(feedback)")
    columns = [col[1] for col in cursor.fetchall()]
    if "comment" not in columns:
        cursor.execute("ALTER TABLE feedback ADD COLUMN comment TEXT")

    # Tabela users (fillimisht pa role)
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

    # Shto kolonën 'role' nëse mungon (safe ALTER)
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    if "role" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")

    # Tabela chat_history
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

def create_user(username: str, email: str, country: str, password: str, role: str = "user"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    hashed_pw = hash_password(password)
    cursor.execute(
        "INSERT INTO users (username, email, country, password, created_at, role) VALUES (?, ?, ?, ?, ?, ?)",
        (username, email, country, hashed_pw, created_at, role)
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

def get_user_by_username(username: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, role FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    print("Kerkim DB:", row)  # <-- Debug print!
    if row:
        return {"id": row[0], "username": row[1], "password": row[2], "role": row[3]}
    return None

def insert_feedback(question, answer, rating, username=None, comment=None):
    quality_score = compute_quality_score(question, answer)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO feedback (question, answer, rating, username, quality_score, comment)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (question, answer, rating, username, quality_score, comment))
    conn.commit()
    conn.close()

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

if __name__ == "__main__":
    init_db()
    print("Database migrated (role checked/added)!")
