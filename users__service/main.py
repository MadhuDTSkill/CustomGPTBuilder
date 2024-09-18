from fastapi import FastAPI
from src.routes import auth_router
from src.components.db import init_db
from contextlib import contextmanager

app = FastAPI()

init_db()
# Include the auth routes
app.include_router(auth_router, prefix="/auth", )


@app.get("/", tags=["General"])
async def root():
    return {"message": "Welcome to the User Service API!"}
