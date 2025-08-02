from fastapi import FastAPI
from routes import stats, auth_routes, feedback, ask
from data.database import init_db

app = FastAPI()

# Inicializo databazën
init_db()

# Rregullo këtë pjesë siç duhet
app.include_router(auth_routes.router)  # Mos e quaj 'auth_router' nëse nuk e ke importuar me atë emër
app.include_router(ask.router)
app.include_router(feedback.router)
app.include_router(stats.router)