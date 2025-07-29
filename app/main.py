from fastapi import FastAPI
from routes import ask
from routes import feedback
from routes import stats
from data.database import insert_feedback, init_db
from routes import stats

app = FastAPI()

# Inicializo DB kur nis app-i
init_db()

# Routes
app.include_router(ask.router)
app.include_router(feedback.router)
app.include_router(stats.router)