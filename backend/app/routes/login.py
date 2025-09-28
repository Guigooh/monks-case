from fastapi import APIRouter, HTTPException
from ..models import LoginIn
from ..auth import authenticate_user, create_access_token

router = APIRouter(prefix="/api", tags=["auth"])

@router.post("/login")
async def login(payload: LoginIn):
    user = authenticate_user(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = create_access_token({"sub": user["email"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}
