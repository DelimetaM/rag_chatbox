from fastapi import FastAPI
from routes import ask

app = FastAPI()

app.include_router(ask.router)  # kjo do funksionojë vetëm nëse ask.py ka router