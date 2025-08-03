from fastapi import FastAPI
from routes import stats, auth_routes, feedback, ask, weights
from data.database import init_db
from app.limiter import limiter  
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

app = FastAPI()
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Ke kaluar limitin e lejuar të kërkesave! Provo sërish pas pak."}
    )

init_db()
app.include_router(auth_routes.router)
app.include_router(ask.router)
app.include_router(feedback.router)
app.include_router(stats.router)
app.include_router(weights.router)
