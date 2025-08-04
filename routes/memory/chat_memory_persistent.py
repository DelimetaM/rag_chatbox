import os
import json
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict

# Folderi ku do ruhen historitë
CHAT_HISTORY_DIR = os.path.join(os.path.dirname(__file__), "../../data/chat_histories")
os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)

class UserChatMemory:
    def __init__(self, username: str):
        self.username = username
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dim = self.model.get_sentence_embedding_dimension()  # 384
        self.index = faiss.IndexFlatL2(self.dim)
        self.data: List[Dict[str, str]] = []
        self._load_from_disk()

    def _get_file_path(self):
        return os.path.join(CHAT_HISTORY_DIR, f"{self.username}.json")

    def _load_from_disk(self):
        """Ngarkon historikun dhe FAISS index nga file."""
        path = self._get_file_path()
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
            # Rikrijo FAISS index nga embedding-et e pyetjeve
            if self.data:
                vectors = self.model.encode([item["question"] for item in self.data], convert_to_numpy=True)
                self.index.add(vectors)
        else:
            self.data = []
            self.index = faiss.IndexFlatL2(self.dim)

    def _save_to_disk(self):
        path = self._get_file_path()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def save_question_answer(self, question: str, answer: str):
        # Kontroll për duplicate
        if any(item["question"] == question for item in self.data):
            return
        vector = self.model.encode([question], convert_to_numpy=True)
        self.index.add(vector)
        self.data.append({"question": question, "answer": answer})
        self._save_to_disk()

    def search_similar_questions(self, question: str, top_k: int = 2) -> List[Dict[str, str]]:
        if not self.data:
            return []
        vector = self.model.encode([question], convert_to_numpy=True)
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

    def get_history(self):
        return list(self.data)

    def clear_history(self):
        self.data = []
        self.index = faiss.IndexFlatL2(self.dim)
        self._save_to_disk()

# Helper për të mos instancuar 1000 herë
__chat_memory_cache = {}
def get_user_chat_memory(username: str) -> UserChatMemory:
    if username not in __chat_memory_cache:
        __chat_memory_cache[username] = UserChatMemory(username)
    return __chat_memory_cache[username]
