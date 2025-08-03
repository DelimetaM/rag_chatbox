import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.auth.auth import authenticate_user, create_access_token, hash_password
from data.database import create_user, user_exists   # Shto importin e ri!
from models.request_models import RegisterUserRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

# ✅ ENDPOINT për regjistrim me kontroll për duplicate
@router.post("/register")
def register(user: RegisterUserRequest):
    # Kontrollo nëse username ose email ekziston
    if user_exists(user.username, user.email):
        raise HTTPException(
            status_code=400,
            detail="Ky username ose email ekziston."
        )
    try:
        create_user(
            username=user.username,
            email=user.email,
            country=user.country if user.country else "",
            password=hash_password(user.password)
        )
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ ENDPOINT për login dhe marrje token
@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
