from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth_service.routers.auth_router import read_users_me
from src.auth_service.schemas import UserPublic, UserCreate, UserUpdate
from src.auth_service.services.user_service import UserService
from src.auth_service.database import get_session


router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, session: AsyncSession = Depends(get_session)):
    try:
        user = await UserService.create_user(
            session=session,
            email=data.email,
            password=data.password,
            role=data.role
        )

        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get('/me', response_model=UserPublic)
async def get_me(current_user=Depends(read_users_me)):
    return current_user


@router.get('/{user_id}', response_model=UserPublic)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await UserService.get_user_by_id(
        session=session,
        user_id=user_id
    )

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    return user


@router.patch('/{user_id}', response_model=UserPublic)
async def update_user(user_id: int, data: UserUpdate, session: AsyncSession = Depends(get_session)):
    user = await UserService.get_user_by_id(
        session=session,
        user_id=user_id
    )

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    updated_user = await UserService.update_user(session, user, **data.model_dump())

    return updated_user


@router.delete('/{user_id}')
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await UserService.get_user_by_id(
        session=session,
        user_id=user_id
    )

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    await UserService.delete_user(
        session=session,
        user=user
    )

    return {'status': 'deleted'}