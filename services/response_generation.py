from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  

def generate_answer(question: str, docs: list, weights: list) -> str:
    if not docs:
        return "Sorry, I couldn't find any good information to answer that."

    # Krijo embeddings për pyetjen
    question_embedding = model.encode([question])

    # Për secilin dokument, llogarisim ngjashmërinë me pyetjen
    ranked_docs = []
    for doc, weight in zip(docs, weights):
        doc_embedding = model.encode([doc["question"]])
        similarity = cosine_similarity([question_embedding[0]], [doc_embedding[0]])[0][0]
        score = similarity * (weight if weight > 0 else 1)  # që të mos jetë zero
        ranked_docs.append((doc, score))

    # Rendit dokumentet sipas score
    ranked_docs.sort(key=lambda x: x[1], reverse=True)

    # Merr dokumentin e parë
    top_doc = ranked_docs[0][0]

    return top_doc["answer"]