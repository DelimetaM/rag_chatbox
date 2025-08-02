import sqlite3
import os
from passlib.context import CryptContext

# Gjej rrugën absolute për databazën
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "feedback.db")

# Konteksti për hash-imin e fjalëkalimeve
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Inicializo databazën
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabela për përdoruesit
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            country TEXT,
            hashed_password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabela për feedback-un
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            rating INTEGER NOT NULL,
            quality_score REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

# ✅ Shto një feedback të ri
def insert_feedback(question: str, answer: str, rating: int, quality_score: float, username: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO feedback (username, question, answer, rating, quality_score)
        VALUES (?, ?, ?, ?, ?)
    """, (username, question, answer, rating, quality_score))
    conn.commit()
    conn.close()

# ✅ Krijo një përdorues të ri
def create_user(username: str, email: str, country: str, password: str):
    hashed_pw = pwd_context.hash(password)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, country, hashed_password) VALUES (?, ?, ?, ?)",
        (username, email, country, hashed_pw)
    )
    conn.commit()
    conn.close()

# ✅ Merr përdorues sipas username
def get_user_by_username(username: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, country, hashed_password, created_at FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "country": row[3],
            "hashed_password": row[4],
            "created_at": row[5]
        }
    return None