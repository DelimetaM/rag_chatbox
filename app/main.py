from fastapi import FastAPI
from routes import ask
from routes import feedback  # shtojmë këtë
from models.database.database import init_db
from routes import stats

app = FastAPI()

# Inicializo DB kur nis app-i
def init_db():
    print("DB initialized (placeholder)")
    
# Routes
app.include_router(ask.router)
app.include_router(feedback.router)  # shtojmë këtë
app.include_router(stats.router)
