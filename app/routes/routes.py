from fastapi import APIRouter

from bot.training.train import start_training
from bot.chat.chat import start_chatting


router = APIRouter()


@router.get('/')
async def root():
    return {'message': 'hello from root'}


@router.get('/train')
async def train_model():
    res = start_training()
    return {'model': res}


@router.get('/chat/{msg}')
async def chat(msg):
    bot_response = start_chatting(msg)
    return {'bot': f'{bot_response}'}
