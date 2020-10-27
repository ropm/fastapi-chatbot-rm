from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'hello from root'}


@app.get('/train/{model_name}')
async def train_model():
    return {'message': 'training model'}


@app.get()
async def start_chat():
    return {'message': 'starting chat with bot x'}
