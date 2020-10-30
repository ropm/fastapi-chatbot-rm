import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'hello from root'}


@app.get('/train/{model_name}')
async def train_model():
    return {'message': 'training model'}


@app.get('/chat/{bot_name}')
async def start_chat(bot_name):
    return {'message': f'starting chat with bot {bot_name}'}


# if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=8000)
