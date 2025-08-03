from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os

# Ngarkimi i modelit te embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Rruga absolute e files faq_data.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(BASE_DIR, "data", "faq_data.json")

# Ngarkimi datasetit nga JSON
with open(data_path, "r", encoding="utf-8") as f:
    faq_data = json.load(f)

# Merr vetëm pyetjet nga dataset
questions = [item["question"] for item in faq_data]
question_embeddings = model.encode(questions)

# Krijo FAISS index
index = faiss.IndexFlatL2(question_embeddings.shape[1])
index.add(np.array(question_embeddings))

# Funksion për embedding të tekstit
def embed_text(text: str):
    return model.encode([text])[0]

# Funksion për cosine similarity
def cosine_similarity(vec1, vec2):
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))

# Funksion për të marrë dokumentet më të mira sipas cosine similarity dhe peshës
def retrieve_top_k_docs(query: str, top_k: int = 5, alpha: float = 0.7, beta: float = 0.3):
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
    return scored_results[:top_k]

# Kthe dokumentin më të afërt
def retrieve_relevant_doc(query: str):
    return retrieve_top_k_docs(query, top_k=1)[0]

# Kthe edhe dokumentet + pyetjet për feedback
def retrieve_relevant_docs(query: str, top_k: int = 5, include_questions: bool = False):
    results = retrieve_top_k_docs(query, top_k=top_k)
    docs = results
    questions = [r["question"] for r in results] if include_questions else []
    return docs, questions

# Merr gjithë datasetin
def get_all_docs():
    return faq_data
