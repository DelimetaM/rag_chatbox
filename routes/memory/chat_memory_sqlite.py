import sqlite3
import os
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DB_PATH = os.path.join(PROJECT_ROOT, "data", "feedback.db")

class UserChatMemory:
    def __init__(self, username: str):
        print("DB_PATH =", DB_PATH)
        print("Exists:", os.path.exists(DB_PATH))
        self.username = username
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dim = self.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(self.dim)
        self.data: List[Dict[str, str]] = []
        self._load_from_db()


    def _load_from_db(self):
        """Ngarkon chat history nga SQLite dhe krijon FAISS index."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT question, answer FROM chat_history WHERE username = ? ORDER BY timestamp ASC",
            (self.username,)
        )
        rows = cursor.fetchall()
        conn.close()
        self.data = [{"question": row[0], "answer": row[1]} for row in rows]
        if self.data:
            vectors = self.model.encode([item["question"] for item in self.data], convert_to_numpy=True)
            self.index.add(vectors)
        else:
            self.index = faiss.IndexFlatL2(self.dim)

    def save_question_answer(self, question: str, answer: str):
        # Kontroll për duplicate (në kujtesë, jo në DB)
        if any(item["question"] == question for item in self.data):
            return
        vector = self.model.encode([question], convert_to_numpy=True)
        self.index.add(vector)
        self.data.append({"question": question, "answer": answer})
        # Ruaj në databazë
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (username, question, answer) VALUES (?, ?, ?)",
            (self.username, question, answer)
        )
        conn.commit()
        conn.close()

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
        # Fshi edhe nga databaza
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM chat_history WHERE username = ?",
            (self.username,)
        )
        conn.commit()
        conn.close()

# Helper cache për të njëjtin user
__chat_memory_cache = {}
def get_user_chat_memory(username: str) -> UserChatMemory:
    if username not in __chat_memory_cache:
        __chat_memory_cache[username] = UserChatMemory(username)
    return __chat_memory_cache[username]
