# 🤖 RAG-powered FAQ Chatbot API with Feedback Loop

Ky projekt ofron një API inteligjente për një **chatbot FAQ**, e cila përdor **Retrieval-Augmented Generation (RAG)** për të gjeneruar përgjigje bazuar në dokumente relevante dhe përmirësohet me kalimin e kohës falë një **sistemi feedback-u nga përdoruesit**.

---

## 📌 Përmbajtja

- [🎯 Qëllimi](#🎯-qëllimi)
- [⚙️ Teknologjitë](#⚙️-teknologjitë)
- [📂 Struktura e projektit](#📂-struktura-e-projektit)
- [🚀 Si ta përdorësh (Docker)](#🚀-si-ta-përdorësh-docker)
- [🔐 Autentikimi (JWT)](#🔐-autentikimi-jwt)
- [📡 Endpoint-et](#📡-endpoint-et)
- [📊 Statistikat e feedback-ut](#📊-statistikat-e-feedback-ut)
- [🧠 Si funksionon feedback loop](#🧠-si-funksionon-feedback-loop)
- [📸 Screenshot-e funksionale](#📸-screenshot-e-funksionale)



## 🎯 Qëllimi

Të krijohet një **backend API** e thjeshtë, por inteligjente, për një chatbot që:
- Gjen pyetjet më të ngjashme në një dataset ekzistues (me FAISS + embeddings)
- Gjeneron përgjigje duke përdorur përmbajtjen e dokumenteve
- Lejon përdoruesit të japin **feedback**
- Mban historikun e bisedës
- Ruhet dhe ekzekutohet përmes **Docker**

---

## ⚙️ Teknologjitë

| Teknologjia           | Përdorimi |
|-----------------------|----------|
| **FastAPI**           | Ndërtimi i API-së REST |
| **SentenceTransformers** | Për embeddings semantikë |
| **FAISS**             | Kërkimi semantik në dokumente |
| **SQLite**            | Baza e të dhënave lokale |
| **JWT + OAuth2**      | Autentikim dhe autorizim |
| **Docker**            | Containerizimi i aplikacionit |

---

## 📂 Struktura e projektit
rag_chatbox/
├── app/
│ └── auth/ # Funksione për login dhe token
├── data/
│ └── database.py # Funksione për SQLite
├── models/
│ └── request_models.py # Pydantic për validim input-i
├── routes/
│ └── endpoints.py # API endpoint-et
├── services/
│ └── retrieval.py # FAISS retrieval
│ └── feedback_loop.py # Përmirësim i rankimit me feedback
├── feedback.db # SQLite database file
├── requirements.txt # Varësitë e projektit
├── dockerfile # Dockerfile për imazhin
├── .dockerignore # Skedarët që përjashtohen nga Docker
└── main.py # Pika hyrëse për API-në

🔐 Autentikimi (JWT)
Endpoint: POST /token
Jepet username dhe password për të marrë JWT token
Endpoint-et që kërkojnë autorizim janë të mbrojtura me OAuth2

📊 Statistikat e feedback-ut
Mesatarja e vlerësimeve
Numri total i feedback-eve
Mund të zgjerohet me analiza të tjera

🧠 Si funksionon feedback loop
Përdoruesi bën një pyetje
Sistemi rikthen dokumentet më relevante
Përdoruesi jep një rating
Pyetja dhe feedback-u ruhen në DB
Algoritmi feedback_loop.py llogarit peshët për secilin dokument dhe përmirëson retrieval-in në pyetjet e ardhshme