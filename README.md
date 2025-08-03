RAG-Powered FAQ Chatbot API (me Feedback Loop, Auth & Docker)

Ky projekt është një API moderne për një chatbot të zgjuar që ofron përgjigje të sakta nga një bazë pyetjesh/FAQ duke përdorur Retrieval-Augmented Generation. Përdoruesit regjistrohen, autentikohen me JWT, bëjnë pyetje, marrin përgjigje dhe japin feedback – gjithçka ruhet dhe përdoret për të përmirësuar cilësinë.

Përmbajtja
Funksionalitetet kryesore:

•	Si instalohet & niset
•	Endpoint-et kryesore
•	Screenshots (Swagger UI)
•	Testim & Demonstrim
•	Teknologjitë e përdorura
•	Struktura e projektit

Funksionalitetet kryesore:
•	Regjistrim dhe login me JWT (OAuth2)
•	Pyetje & përgjigje të mençura nga dataset-i i FAQ-ve (RAG + embeddings)
•	Feedback për çdo përgjigje
•	Rritje cilësie në retrieval/response bazuar në feedback
•	Ruajtje e historikut të bisedës në databazë për çdo user
•	Rate limiting për siguri nga abuzimi
•	Ruajtje të sigurt të fjalëkalimeve (bcrypt hash)
•	Deploy me Docker 


Si instalohet & niset:

Lokalisht (pa Docker)
1. Klono projektin:
git clone https://github.com/DelimetaM/rag_chatbox
cd rag_chatbox

2. Krijo & aktivizo virtualenv:
python -m venv venv
source venv/bin/activate  # ose venv\Scripts\activate në Windows

3. Instalo varësitë:
pip install -r requirements.txt

4. Nise aplikacionin:
uvicorn app.main:app --reload
Hape Swagger UI në browser ose Postman:
http://127.0.0.1:8000/docs


Me Docker

1. Ndërto imazhin Docker:
docker build -t rag_chatbox .

2. Nise me Docker
docker compose up --build


Endpoint-et Kryesore:

/auth/register
[POST]
Regjistron një përdorues të ri.
Auth: JO

/auth/token
[POST]
Login dhe merr JWT token.
Auth: JO

/ask
[POST]
Dërgo pyetje, merr përgjigje nga FAQ dhe pyetje të ngjashme.
Auth: PO (JWT)
Rate limit: 5 pyetje për minutë.

/feedback
[POST]
Jep feedback për një përgjigje.
Auth: PO (JWT)
Rate limit: 5 feedback për minutë.

/chat-history
[GET, DELETE]
Merr ose fshin historikun e bisedës.
Auth: PO (JWT)

Të gjitha endpoint-et (përveç register/login) kërkojnë JWT token në header-in Authorization!


Screenshots (Swagger UI)

1. Regjistrimi i një përdoruesi të ri
[Register Success](screenshots/1.2success_registration.png)
[Register Failed](screenshots/1.failed_registration.png)

2. Login dhe marrje JWT token
[Successful Login](screenshots/2.successful_login.png)
[Successful Authentication](screenshots/2.1%20successful_authentication.png)

3. /ask – Pyetje/Response
[Question](screenshots/3.%20Question.png)
[Answer](screenshots/3.1%20Answer.png)

4. /feedback – Dërgim feedback
[Feedback](screenshots/4.%20Feedback.png)
[Feedback Limit](screenshots/4.1%20Feedback%20Limit.png)

5. /chat-history
[Chat History](screenshots/5.%20Chat%20History.png)
[Chat History Cleared](screenshots/5.1%20Chat%20History%20Cleared.png)


Testim & Demonstrim

1. Regjistrim
•	Dërgo POST në /auth/register me JSON:
{
  "username": "meti",
  "email": "meti@email.com",
  "country": "Albania",
  "password": "TestPassword123!"
}
•	Kontrollo që merr “User registered successfully”.

2. Login
•	POST /auth/token me username/password.
•	Kopjo access_token nga përgjigjja.

3. Pyetje (Ask)
•	POST /ask me JWT në header:
{
  "question": "What is ransomware?",
  "show_related": true
}
•	Kontrollo përgjigjen dhe fushën related_questions.

4. Feedback
•	POST /feedback me JWT në header dhe pyetjen që sapo bëre.

5. Rate limiting
•	Dërgo më shumë se 5 kërkesa për endpoint në 1 minutë.
•	Kontrollo që merr error 429.

6. Historiku
•	GET /chat-history me JWT, kontrollo që shfaqen pyetjet dhe përgjigjet.


Teknologjitë e përdorura

•	FastAPI (backend framework)
•	SQLite (db lokale)
•	JWT/OAuth2 (auth)
•	bcrypt (hashing i fjalëkalimeve)
•	sentence-transformers + faiss (RAG, retrieval)
•	Docker (deployment)
•	slowapi (rate limiting)
•	Swagger UI (dokumentim/testim API)


Struktura e projektit

rag_chatbox/
├── app/
│   ├── main.py
│   ├── limiter.py
│   └── auth/
├── data/
│   ├── feedback.db
│   ├── database.py
│   └── faq_data.json
├── models/
│   └── request_models.py
├── routes/
│   ├── ask.py
│   ├── feedback.py
│   └── ...
├── requirements.txt
├── Dockerfile
└── README.md