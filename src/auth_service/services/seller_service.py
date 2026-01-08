from sqlalchemy.ext.asyncio import AsyncSession

from models import Seller


class SellerService:
    @staticmethod
    async def create_seller(session: AsyncSession, user_id: int, name: str, phone: str):
        seller = Seller(
            id=user_id,
            name=name,
            phone=phone,
            rating=0.0
        )
        session.add(seller)
        await session.commit()
        await session.refresh(seller)

        return seller
