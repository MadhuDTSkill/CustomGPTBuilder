from fastapi import FastAPI
from contextlib import contextmanager
from src.routes import chat_router
app = FastAPI()


app.include_router(chat_router, prefix="/chat", )




