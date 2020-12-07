import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import routes


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.include_router(routes.router, prefix='/api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=8000)
