from sqlmodel import Field, SQLModel, Column
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID
import uuid

class User(SQLModel, table=True):
    uuid: UUID = Field(
        default_factory=uuid.uuid4,  # Use default_factory for UUID generation
        sa_column=Column(pg.UUID, nullable=False, primary_key=True)
    )
    username: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
