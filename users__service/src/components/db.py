import os
from sqlmodel import create_engine, SQLModel, text

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    with engine.begin() as conn:
        from .models import User
        SQLModel.metadata.create_all(engine)


