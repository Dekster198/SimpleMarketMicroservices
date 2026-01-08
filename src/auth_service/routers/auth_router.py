from datetime import timedelta
from fastapi import APIRouter, status, HTTPException
from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth_service import OAuth2PasswordRequestFormWithEmail, Token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user
from models import User, UserRole
from schemas import UserPublic, UserCreate
from services.buyer_service import BuyerService
from services.seller_service import SellerService
from services.user_service import UserService
from database import get_session


router = APIRouter()


@router.post("/register", response_model=UserPublic)
async def register(data: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await UserService.create_user(
        session=session,
        email=data.email,
        password=data.password,
        role=data.role
    )

    if data.role == UserRole.seller:
        await SellerService.create_seller(
            session=session,
            user_id=user.id,
            name=data.name,
            phone=data.phone
        )
    elif data.role == UserRole.buyer:
        await BuyerService.create_buyer(
            session=session,
            user_id=user.id,
            name=data.name,
            phone=data.phone
        )

    return user


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestFormWithEmail, Depends()],
                                 session: Annotated[AsyncSession, Depends(get_session)]) -> Token:
    """эндпоинт для получения токена"""
    user = await authenticate_user(session, form_data.email, form_data.password)  # аутентификация пользователя
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserPublic)
async def me(user: Annotated[User, Depends(get_current_user)]):
    return user


@router.get("/users/me/items/")
async def read_own_items(
        current_user: Annotated[User, Depends(get_current_user)],
):
    return [{"item_id": "Foo", "owner": current_user.email}]
