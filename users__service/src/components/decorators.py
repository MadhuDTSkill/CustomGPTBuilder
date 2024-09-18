from functools import wraps
from fastapi import Request, HTTPException, status
from .jwt_token import verify_token

def authenticate(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        # Extract the token from the Authorization header
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication token is missing")

        # Remove the "Bearer " prefix if present
        if token.startswith("Bearer "):
            token = token[len("Bearer "):]
        
        # Verify the token
        payload = verify_token(token)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")

        # Add the payload to kwargs if needed by the actual function
        kwargs['user_payload'] = payload

        # Call the actual function with the original arguments and keyword arguments
        return await func(request, *args, **kwargs)
    
    return wrapper
