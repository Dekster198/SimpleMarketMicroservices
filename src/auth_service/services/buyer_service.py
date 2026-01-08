from sqlalchemy.ext.asyncio import AsyncSession

from models import Buyer


class BuyerService:
    @staticmethod
    async def create_buyer(session: AsyncSession, user_id: int, name: str, phone: str):
        buyer = Buyer(
            id=user_id,
            name=name,
            phone=phone
        )
        session.add(buyer)
        await session.commit()
        await session.refresh(buyer)

        return buyer
