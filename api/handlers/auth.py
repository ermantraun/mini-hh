from fastapi import APIRouter, HTTPException
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from api.schemas.user import RegisterRequest, TokenResponse, UserOut
from application.user.interactors import AuthInteractor
from application.user.exceptions import RegistrationError, AuthenticationError

router = APIRouter(prefix="/auth", tags=["auth"], route_class=DishkaRoute)

@router.post("/register", response_model=UserOut, status_code=201)
async def register(payload: RegisterRequest, interactor: FromDishka[AuthInteractor]):
    # Добавлена ручная валидация для получения 400 (а не 422) в тесте
    if "@" not in payload.email:
        raise HTTPException(status_code=400, detail="Invalid email")
    if len(payload.password) < 6:
        raise HTTPException(status_code=400, detail="Password too short")
    try:
        user = await interactor.register(payload.email, payload.password)
        return UserOut(id=user.id, email=user.email)
    except RegistrationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
async def login(payload: RegisterRequest, interactor: FromDishka[AuthInteractor]):
    try:
        token = await interactor.login(payload.email, payload.password)
        return TokenResponse(access_token=token)
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))