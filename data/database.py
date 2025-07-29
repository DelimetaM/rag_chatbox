import sqlite3
import os

# Gjej rrugën për ruajtjen e db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "feedback.db")

# Funksion për inicializim të tabelës
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            rating INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Funksion për shtim të feedback
def insert_feedback(question: str, answer: str, rating: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO feedback (question, answer, rating)
        VALUES (?, ?, ?)
    """, (question, answer, rating))
    conn.commit()
    conn.close()