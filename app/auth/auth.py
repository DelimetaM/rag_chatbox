import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from data.database import get_user_by_username
from passlib.context import CryptContext

# Sekretet për JWT
SECRET_KEY = "sekret_super_i_sigurt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# URL për Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Konteksti për hashimin e fjalëkalimit
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HASH
def hash_password(password: str):
    return pwd_context.hash(password)

# VERIFIKIM HASH
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# AUTENTIKIM USERI NGA DATABASE
def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user or not verify_password(password, user["password"]):
        return None
    return user

# KRIJO TOKEN JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# MERR USERIN NGA TOKEN
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user_by_username(username)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token error")

# --- KONTROLLI PER ADMIN ---
def admin_required(user=Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden: admin only")
    return user
