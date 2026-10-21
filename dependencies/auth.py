from fastapi import Header, HTTPException, status

ACTIVE_TOKENS: dict[str, str] = {}


def get_current_user(authorization: str | None = Header(default=None)) -> str:
    """Return the username for a valid 'Authorization: Bearer <token>' header, else 401."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    token = authorization.removeprefix("Bearer ")
    username = ACTIVE_TOKENS.get(token)
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return username