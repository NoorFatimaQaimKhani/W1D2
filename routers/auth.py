import secrets

from fastapi import APIRouter, Depends, HTTPException, status

from dependencies.auth import ACTIVE_TOKENS, get_current_user
from schemas.auth import LoginRequest, LoginResponse, MeResponse

router = APIRouter(prefix="/auth", tags=["auth"])

# Synthetic users for practice purposes.
FAKE_USERS = {"teacher01": "Password123", "admin01": "Admin12345"}


@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest) -> LoginResponse:
    # Same error for a wrong password and an unknown user, so nobody can find out which users exist.
    if FAKE_USERS.get(body.username) != body.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token = secrets.token_hex(16)
    ACTIVE_TOKENS[token] = body.username
    return LoginResponse(access_token=token)


@router.get("/me", response_model=MeResponse)
def me(username: str = Depends(get_current_user)) -> MeResponse:
    return MeResponse(username=username)