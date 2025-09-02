from datetime import datetime, timedelta, timezone
import jwt
from api.config import get_config


def create_access_token(sub: str) -> str:
    cfg = get_config().jwt
    exp = datetime.now(timezone.utc) + timedelta(minutes=cfg.access_minutes)
    return jwt.encode({"sub": sub, "exp": exp}, cfg.secret_key, algorithm=cfg.algorithm)


def parse_token(token: str) -> str | None:
    cfg = get_config().jwt
    try:
        payload = jwt.decode(token, cfg.secret_key, algorithms=[cfg.algorithm])
        return payload.get("sub")
    except Exception:
        return None