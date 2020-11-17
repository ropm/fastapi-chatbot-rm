import json
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from bot.training.train import start_training
from bot.chat.chat import start_chatting

from app.db import schemas, models, model_operations
from app.db.database import get_db


router = APIRouter()


@router.get('/train')
def train_model(epochs: Optional[int] = None, db: Session = Depends(get_db), user: schemas.User = Depends(model_operations.get_current_active_user)):
    intent = model_operations.get_intents(db=db)
    if not epochs:
        epochs = 2000
    res = start_training(intent.intents, epochs)
    return {'model': res}


@router.get('/chat/{msg}')
async def chat(msg, db: Session = Depends(get_db)):
    intent = model_operations.get_intents(db=db)
    bot_response = start_chatting(msg, intent.intents)
    return {'bot': f'{bot_response}'}


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, key: str, db: Session = Depends(get_db)):
    db_user = model_operations.get_user_by_email(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    return model_operations.create_user(db=db, user=user, key=key)


@router.post('/intents-file/')
def save_intents(intents_file: UploadFile = File(...), db: Session = Depends(get_db), user: schemas.User = Depends(model_operations.get_current_active_user)):
    contents = intents_file.file.read()
    #contents_json = json.loads(contents)
    model_to_save = {'intents': contents, 'description': 'Test'}
    intents = schemas.IntentCreate(**model_to_save)
    return model_operations.create_intents(db=db, intent=intents)


@router.get('/intents/')
def get_latest_intents(db: Session = Depends(get_db), user: schemas.User = Depends(model_operations.get_current_active_user)):
    return model_operations.get_intents(db=db)


@router.post('/token', response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = model_operations.authenticate_user(
        db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=model_operations.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = model_operations.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
