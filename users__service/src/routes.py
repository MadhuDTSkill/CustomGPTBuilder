from fastapi import APIRouter, status, HTTPException, Depends, Request
from sqlmodel import Session
from .components.schema import UserCreate, UserOut, UserLogin, LoginResponse
from .components.user_manager import UserManager
from .components.dependencies import get_session
from .components.decorators import authenticate

auth_router = APIRouter(tags = ['Authentication'])

@auth_router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(user_data : UserLogin, db: Session = Depends(get_session)):
    user_manager = UserManager(db)
    return user_manager.authenticate_user(**user_data.model_dump())

@auth_router.post("/register", response_model= UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_data : UserCreate, db: Session = Depends(get_session)):
    user_manager = UserManager(db)
    try:
        return user_manager.create_user(**user_data.model_dump())
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, repr(e))

@auth_router.get("/get_user", response_model=UserOut)
@authenticate
async def get_user(request : Request, user_payload:dict = None):
    return user_payload
