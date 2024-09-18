from fastapi import APIRouter, status, HTTPException, Depends, Request
from sqlmodel import Session
from .components.schema import Query, AIResponse
from .components.dependencies import get_session
from .components.decorators import authenticate
from .components.classes import CustomGPTBuilder

chat_router = APIRouter(tags = ['Chat'])

@chat_router.post("/custom_gpt_builder", response_model=AIResponse, status_code=status.HTTP_200_OK)
@authenticate
async def custom_gpt_builder(request : Request, query : Query, db: Session = Depends(get_session), user_payload : dict = None):
    assistance = CustomGPTBuilder(user_id = user_payload["uuid"])
    ai_response = assistance.run(query.model_dump()["query"])
    return {"response":ai_response}

