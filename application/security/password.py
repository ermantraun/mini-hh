from passlib.context import CryptContext

_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(p: str) -> str:
    return _ctx.hash(p)


def verify_password(plain: str, hashed: str) -> bool:
    return _ctx.verify(plain, hashed)