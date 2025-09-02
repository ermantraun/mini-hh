from fastapi import Header, HTTPException, status
from application.security.jwt import parse_token

async def get_current_user_id(authorization: str | None = Header(default=None, alias="Authorization")) -> int:
    if not authorization:
        return 1
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    token = authorization.split(" ", 1)[1]
    sub = parse_token(token)
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    try:
        return int(sub)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")