from pydantic import BaseModel



class Query(BaseModel):
    query : str
    
class AIResponse(BaseModel):
    response : str
