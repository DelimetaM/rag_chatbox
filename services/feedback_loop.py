import sqlite3
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# modeli që përdor për embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

def calculate_question_embedding(question: str):
    return model.encode([question])[0]

def compute_feedback_weights(question: str, docs: list):
    conn = sqlite3.connect("data/feedback.db")
    cursor = conn.cursor()
    cursor.execute("SELECT question, rating FROM feedback")
    feedback_entries = cursor.fetchall()
    conn.close()

    weights = []
    for doc in docs:
        score = 0
        for feedback_question, rating in feedback_entries:
            sim = cosine_similarity(
                [calculate_question_embedding(doc)],
                [calculate_question_embedding(feedback_question)]
            )[0][0]
            score += sim * rating
        weights.append(score)
    
    return weights