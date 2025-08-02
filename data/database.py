import sqlite3
import os

# Gjej rrugën absolute për databazën
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "feedback.db")

# Funksion për inicializim të tabelës (me kontroll për quality_score)
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Krijo tabelën nëse nuk ekziston
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            rating INTEGER NOT NULL
        )
    """)

    # Kontrollo nëse kolona quality_score ekziston dhe shtoje nëse mungon
    cursor.execute("PRAGMA table_info(feedback)")
    columns = [col[1] for col in cursor.fetchall()]
    if "quality_score" not in columns:
        cursor.execute("ALTER TABLE feedback ADD COLUMN quality_score REAL")

    conn.commit()
    conn.close()

# Funksion për futje të feedback-it me quality_score
def insert_feedback(question: str, answer: str, rating: int, quality_score: float):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO feedback (question, answer, rating, quality_score)
        VALUES (?, ?, ?, ?)
    """, (question, answer, rating, quality_score))
    conn.commit()
    conn.close()