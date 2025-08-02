from fastapi import FastAPI
from routes import stats, auth_routes, feedback, ask
from data.database import insert_feedback, init_db

app = FastAPI()


# Inicializo DB kur nis app-i
init_db()

# Routes
app.include_router(auth_routes.router)
app.include_router(ask.router)
app.include_router(feedback.router)
app.include_router(stats.router)