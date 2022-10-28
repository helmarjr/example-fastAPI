from . import models
from fastapi import FastAPI
from .routers import post, user, auth, vote
from .database import engine
from fastapi.middleware.cors import CORSMiddleware


# Models
models.Base.metadata.create_all(bind=engine)

origins = ['*']

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/', tags=['Root'])
def root():
    return {'data': 'rota pricipal'}

# uvicorn main:app --reload
# uvicorn app.main:app --reload
# http://127.0.0.1:8000/redoc
# http://127.0.0.1:8000/docs

# Teste de CORS via console no Browser
# fetch('http://localhost:8000/').then(res => res.json()).then(console.log)