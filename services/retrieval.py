from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os
from difflib import SequenceMatcher

# --- Ngarko modelin dhe datasetin ---
model = SentenceTransformer('all-MiniLM-L6-v2')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(BASE_DIR, "data", "faq_data.json")

with open(data_path, "r", encoding="utf-8") as f:
    faq_data = json.load(f)

def ultra_normalize(text):
    return ' '.join(text.lower().strip().split())

def fuzzy_match(q1, q2, threshold=0.80):
    return SequenceMatcher(None, ultra_normalize(q1), ultra_normalize(q2)).ratio() >= threshold

def embed_text(text: str):
    return model.encode([text])[0]

def cosine_similarity(vec1, vec2):
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))

questions = [item["question"] for item in faq_data]
question_embeddings = np.array([embed_text(q) for q in questions])
index = faiss.IndexFlatL2(question_embeddings.shape[1])
index.add(np.array(question_embeddings))

def retrieve_top_k_docs(query: str, top_k: int = 5, alpha: float = 0.7, beta: float = 0.3):
    query_norm = ultra_normalize(query)
    
    # 1. EXACT MATCH (shpejt & saktë)
    for item in faq_data:
        if ultra_normalize(item["question"]) == query_norm:
            print("[DEBUG] EXACT MATCH!")
            return [item]
    
    # 2. FUZZY MATCH (similarity >= 0.8)
    for item in faq_data:
        if fuzzy_match(item["question"], query):
            print("[DEBUG] FUZZY MATCH!")
            return [item]
    
    # 3. EMBEDDING SIMILARITY (backup)
    query_embedding = embed_text(query)
    scored_results = []
    for i, item in enumerate(faq_data):
        doc_embedding = question_embeddings[i]
        sim = cosine_similarity(query_embedding, doc_embedding)
        weight = float(item.get("weight", 0.0))
        score = alpha * sim + beta * weight
        scored_results.append({
            "id": item.get("id"),
            "question": item["question"],
            "answer": item["answer"],
            "score": score,
            "original_similarity": sim,
            "weight": weight
        })
    scored_results.sort(key=lambda x: x["score"], reverse=True)
    print("[DEBUG] USING EMBEDDINGS (no exact/fuzzy match)")
    return scored_results[:top_k]

def retrieve_relevant_doc(query: str):
    return retrieve_top_k_docs(query, top_k=1)[0]

def retrieve_relevant_docs(query: str, top_k: int = 5, include_questions: bool = False):
    results = retrieve_top_k_docs(query, top_k=top_k)
    docs = results
    questions = [r["question"] for r in results] if include_questions else []
    return docs, questions

def get_all_docs():
    return faq_data
