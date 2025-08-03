from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Inicializo modelin një herë
model = SentenceTransformer("all-MiniLM-L6-v2")

def normalize_text(text: str) -> str:
    """Normalizon tekstin: heq whitespaces të tepërta, bën lower-case dhe bashkon fjalitë."""
    return " ".join(text.strip().lower().split())

def compute_quality_score(question: str, answer: str) -> float:
    # Normalizo tekstet para embeddings
    question_norm = normalize_text(question)
    answer_norm = normalize_text(answer)

    question_emb = model.encode([question_norm])[0].reshape(1, -1)
    answer_emb = model.encode([answer_norm])[0].reshape(1, -1)

    similarity = cosine_similarity(question_emb, answer_emb)[0][0]
    return round(float(similarity), 2)