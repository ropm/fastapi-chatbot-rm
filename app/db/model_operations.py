from datetime import datetime, timedelta
from typing import Optional
import os
import sys

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from jose import JWTError, jwt

from app.db import models, schemas
from app.db.database import get_db

from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = "af682638ad53df100ed532871a967e4d256842ee93d5d3a8981a4a9e7948161e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
KEY_FOR_CREATE = os.getenv("KEY_CREATE")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user_by_email(db: Session, username: str) -> schemas.User:
    return db.query(models.User).filter(models.User.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_email(db=db, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return current_user


def create_user(db: Session, user: schemas.UserCreate, key: str):
    print(KEY_FOR_CREATE)
    if not key or key != KEY_FOR_CREATE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate the keys",
        )
    passw = get_password_hash(user.password)
    print(passw)
    db_user = models.User(
        username=user.username, hashed_password=passw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_intents(db: Session):
    return db.query(models.Intent).order_by(models.Intent.id.desc()).first()


def create_intents(db: Session, intent: schemas.IntentCreate):
    db_intent = models.Intent(
        description=intent.description, intents=intent.intents)
    db.add(db_intent)
    db.commit()
    db.refresh(db_intent)
    return db_intent
