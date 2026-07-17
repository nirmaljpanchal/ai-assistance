from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Assistance Platform",
    description="Enterprise AI assistance platform API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "AI Assistance Platform API"}


@app.get("/health")
def health_check() -> dict[str, Any]:
    return {"status": "ok", "version": "0.1.0"}
