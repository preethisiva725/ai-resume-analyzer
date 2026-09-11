from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from . import models
from .routers import analysis
from .routers import resume


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Resume Analyzer"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    analysis.router
)

app.include_router(
    resume.router
)


@app.get("/")
def home():
    return {
        "message": "AI Resume Analyzer API is running!"
    }