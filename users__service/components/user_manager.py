from fastapi import HTTPException, status
from sqlmodel import Session, select
from .models import User
from passlib.context import CryptContext
from .jwt_token import create_access_token, create_refresh_token, verify_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserManager:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, username: str, email: str, password: str) -> User:
        hashed_password = self._hash_password(password)
        user = User(username=username, email=email, hashed_password=hashed_password)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def authenticate_user(self, username : str, password:str):
        user = self.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User Not Found")
        result = self.verify_password(plain_password=password, hashed_password=user.hashed_password)
        if not result:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password seems to be wrong!")
        access_token : str = create_access_token(user.model_dump())
        refresh_token : str = create_refresh_token(user.model_dump())
        return {
            "access" : access_token,
            "refresh" : refresh_token
        }

    def get_user_by_username(self, username: str) -> User:
        statement = select(User).where(User.username == username)
        result = self.session.exec(statement)
        return result.one_or_none()

    def _hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def update_password(self, username: str, new_password: str) -> User:
        user = self.get_user_by_username(username)
        if user:
            user.hashed_password = self._hash_password(new_password)
            self.session.commit()
            self.session.refresh(user)
        return user

    def delete_user(self, username: str) -> None:
        user = self.get_user_by_username(username)
        if user:
            self.session.delete(user)
            self.session.commit()
