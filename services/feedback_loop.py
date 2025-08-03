import sqlite3
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Modeli për embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# Merr embedding të një teksti
def embed(text: str):
    return model.encode([text])[0]

# Llogarit peshat për një listë dokumentesh në raport me një query
def compute_feedback_weights(query: str, docs: list):
    # Hap lidhjen me databazën
    conn = sqlite3.connect("data/feedback.db")
    cursor = conn.cursor()
    cursor.execute("SELECT question, rating FROM feedback")
    feedback_entries = cursor.fetchall()
    conn.close()

    # Embedding për query-n e përdoruesit
    query_embedding = embed(query)

    # Embeddings për dokumentet
    doc_embeddings = [embed(doc["question"]) for doc in docs]

    # Embeddings për feedback questions
    feedback_embeddings = [(embed(q), rating) for q, rating in feedback_entries]

    # Llogarit peshat për çdo dokument
    weights = []
    for doc_vec in doc_embeddings:
        score = 0.0
        for fb_vec, rating in feedback_embeddings:
            sim = cosine_similarity([doc_vec], [fb_vec])[0][0]
            score += sim * (rating / 10.0)  # Normalizim rating në [0.1 - 1.0]
        weights.append(score)

    return weights