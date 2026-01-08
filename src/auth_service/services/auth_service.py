import datetime
from datetime import timezone, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status, APIRouter, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from decouple import config
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import argon2

from models import User
from schemas import UserPublic

from database import get_session

router = APIRouter()


class OAuth2PasswordRequestFormWithEmail(OAuth2PasswordRequestForm):
    """
    Custom form that uses email but maintains compatibility with Swagger UI
    """

    def __init__(
            self,
            username: str = Form(..., description="User email"),  # Swagger ожидает username
            password: str = Form(...),
    ):
        # Use username as email for Swagger compatibility
        super().__init__(username=username, password=password)
        self.email = username  # создаём поле email, которое ссылается на username


SECRET_KEY = config('SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    """модель ответа для эндпоинта /token"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """модель для данных внутри JWT-токена"""
    email: str | None = None


ph = argon2.PasswordHasher()  # создание объекта хэшера
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')  # создание OAuth2-схемы, которая указывает на эндроинт /token


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """проверяет, соответствует ли plain_password хэшу"""
    try:
        return ph.verify(hashed_password, plain_password)
    except argon2.exceptions.VerifyMismatchError:
        return False
    except argon2.exceptions.InvalidHashError as e:
        return False


def get_password_hash(password: str) -> str:
    """создаёт хэш пароля (для регистрации пользователей)"""
    return ph.hash(password)


async def get_user(session: AsyncSession, email: str):
    """ищет пользователя по email в базе данных"""
    statement = select(User).where(User.email == email)
    user = await session.execute(statement)

    return user.scalar_one_or_none()


async def authenticate_user(session: AsyncSession, email: str, password: str):
    """аутентифицирует пользователя (проверяет email и password)"""
    user = await get_user(session, email)

    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """функция создания JWT-токена"""
    to_encode = data.copy()  # копируем данные для кодирования

    if expires_delta:  # устанавливаем время истечения токена
        expire = datetime.datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})  # добавляем поле истечения токена
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # кодриуем данные в JWT-токен

    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(get_session)):
    """
    получение текущего пользователя
    token: Annotated[str, Depends(oauth2_scheme)] - зависимость, которая извлекает token из header Authorization
    """
    credentials_exception = HTTPException(  # определение исключения
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # декодируем и проверяем JWT-токен
        email = payload.get("sub")  # извлекаем email из поля sub(subject) токена
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(session, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
