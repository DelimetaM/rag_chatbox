import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict

class ChatMemory:
    def __init__(self):
        # Inicializo modelin dhe FAISS index-in me dimensionin e MiniLM (384)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dim = self.model.get_sentence_embedding_dimension()  # 384
        self.index = faiss.IndexFlatL2(self.dim)
        self.data: List[Dict[str, str]] = []

    def save_question_answer(self, question: str, answer: str):
        """
        Shton pyetjen + përgjigjen në historik, vetëm nëse nuk ekziston më parë.
        """
        # Kontroll për duplicate
        if any(item["question"] == question for item in self.data):
            return
        # Gjej embedding dhe shto në index
        vector = self.model.encode([question], convert_to_numpy=True)
        self.index.add(vector)
        # Ruaj metadata-n
        self.data.append({"question": question, "answer": answer})

    def search_similar_questions(self, question: str, top_k: int = 3) -> List[Dict[str, str]]:
        """
        Kthen listën e top_k çift pyetje-përgjigje nga historiku,
        më të ngjashme me query-n e dhënë.
        """
        if not self.data:
            return []

        # Përgatis vector-in e query
        vector = self.model.encode([question], convert_to_numpy=True)
        # Kerkim në FAISS
        distances, indices = self.index.search(vector, min(top_k, len(self.data)))
        results = []
        seen = set()
        for idx in indices[0]:
            if idx < len(self.data):
                item = self.data[idx]
                if item["question"] not in seen:
                    results.append(item)
                    seen.add(item["question"])
        return results

    def get_history(self) -> List[Dict[str, str]]:
        """Kthen të gjithë historikun në rendin e shtimit."""
        return list(self.data)

    def clear_history(self):
        """Pastron historikun dhe FAISS index-in."""
        self.data = []
        # Rekrijo index-in
        self.index = faiss.IndexFlatL2(self.dim)

# Singleton për të gjithë aplikacionin
memory = ChatMemory()