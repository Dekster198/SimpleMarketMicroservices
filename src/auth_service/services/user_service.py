from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from .auth_service import get_password_hash


class UserService:
    @staticmethod
    async def create_user(session: AsyncSession, email: str, password: str, role) -> User:
        existing = await UserService.get_user_by_email(session, email)
        if existing:
            raise ValueError('Email already in use')

        hashed = get_password_hash(password)

        user = User(
            email=email,
            hashed_password=hashed,
            role=role
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user

    @staticmethod
    async def get_user_by_email(session: AsyncSession, email) -> User:
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)

        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)

        return result.scalar_one_or_none()

    @staticmethod
    async def update_user(session: AsyncSession, user: User, **data) -> User:
        ALLOWED_FIELDS = {'email', 'role'}

        for attr, value in data.items():
            if value in ALLOWED_FIELDS and value is not None:
                setattr(user, attr, value)

        await session.commit()
        await session.refresh(user)

        return user

    @staticmethod
    async def delete_user(session: AsyncSession, user: User) -> None:
        await session.delete(user)
        await session.commit()
