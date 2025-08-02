import sys
import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta
from jose import JWTError, jwt

from app.auth.auth import (
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from data.database import create_user, get_user_by_username
from models.request_models import RegisterUserRequest

# 🛡️ Parametrat për JWT
SECRET_KEY = "sekret_super_i_sigurt"
ALGORITHM = "HS256"

# 🧠 Endpoint që Swagger UI përdor për të marrë token: /auth/token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# 📦 Router për autentikim
router = APIRouter(prefix="/auth", tags=["Auth"])


# ✅ Endpoint për regjistrim të përdoruesit të ri
@router.post("/register")
def register(user: RegisterUserRequest):
    # Kontroll nëse ekziston username-i
    existing_user = get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username ekziston tashmë"
        )

    # Regjistro user-in me password të hash-uar
    create_user(
        username=user.username,
        email=user.email,
        country=user.country,
        password=user.password  # ➜ hashimi bëhet brenda create_user
    )

    # Krijo token direkt pas regjistrimit
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# ✅ Endpoint për login dhe gjenerim token
@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Emër përdoruesi ose fjalëkalim i pasaktë",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


# ✅ Funksion për të marrë përdoruesin aktual nga token (përdoret në endpoint-e të mbrojtura)
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token i pavlefshëm",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(username)
    if user is None:
        raise credentials_exception

    return user