import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict

class ChatMemory:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(384)  # dimensioni i MiniLM
        self.data: List[Dict[str, str]] = []

    def save_question_answer(self, question: str, answer: str):
        # Mos e shto nëse ekziston pyetja
        if any(item["question"] == question for item in self.data):
            return
        vector = self.model.encode([question])
        self.index.add(vector)
        self.data.append({"question": question, "answer": answer})

    def search_similar_questions(self, question: str, top_k: int = 3) -> List[Dict[str, str]]:
        if not self.data:
            return []

        vector = self.model.encode([question])
        distances, indices = self.index.search(vector, min(top_k, len(self.data)))
        results = []
        seen_questions = set()

        for idx in indices[0]:
            if idx < len(self.data):
                item = self.data[idx]
                if item["question"] not in seen_questions:
                    results.append(item)
                    seen_questions.add(item["question"])
        return results

    def get_history(self):
        return self.data

    def clear_history(self):
        self.data = []
        self.index.reset()