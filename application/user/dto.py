from dataclasses import dataclass

# DTO для application слоя; transport слой использует свои pydantic схемы.

@dataclass
class RegisterRequestDTO:
    email: str
    password: str


@dataclass
class TokenResponseDTO:
    access_token: str
    token_type: str = "bearer"


@dataclass
class UserOutDTO:
    id: int
    email: str