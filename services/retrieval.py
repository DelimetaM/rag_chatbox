from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os

# Ngarko modelin e embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Gjej rrugën absolute të fajllit faq_data.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(BASE_DIR, "data", "faq_data.json")

# Ngarko datasetin nga JSON
with open(data_path, "r", encoding="utf-8") as f:
    faq_data = json.load(f)

# Merr vetëm pyetjet nga dataset
questions = [item["question"] for item in faq_data]
embeddings = model.encode(questions)

# Krijo FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

# Funksion që gjen dokumentin më të afërt
def retrieve_relevant_docs(query: str):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), k=1)
    idx = I[0][0]
    return faq_data[idx]