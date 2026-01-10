from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Product

from models import Seller


class ProductService:
    @staticmethod
    async def create_product(
            session: AsyncSession,
            title: str,
            description: str | None,
            price: Decimal,
            quantity: int,
            seller_id: int
    ) -> Product:
        stmt_exists_seller = select(Seller).where(Seller.id == seller_id)
        exists_seller = await session.execute(stmt_exists_seller)
        exists_seller = exists_seller.scalar_one_or_none()

        if not exists_seller:
            raise ValueError('Seller does not exists')

        product = Product(
            title=title,
            description=description,
            price=price,
            quantity=quantity,
            seller_id=seller_id
        )
        session.add(product)
        await session.commit()
        await session.refresh(product)

        return product

    @staticmethod
    async def get_product_by_id(session: AsyncSession, product_id: int) -> Product | None:
        stmt = select(Product).where(Product.id == product_id)
        result = await session.execute(stmt)

        return result.scalar_one_or_none()

    @staticmethod
    async def get_product_by_title(session: AsyncSession, title: str) -> list[Product]:
        stmt = select(Product).where(Product.title == title)
        result = await session.execute(stmt)

        return list(result.scalars().all())

    @staticmethod
    async def get_product_by_seller(session: AsyncSession, seller_id: int) -> list[Product]:
        stmt = select(Product).where(Product.seller_id == seller_id)
        result = await session.execute(stmt)

        return list(result.scalars().all())

    @staticmethod
    async def update_product(session: AsyncSession, product: Product, **data) -> Product:
        ALLOWED_FIELDS = {"title", "description", "price", "quantity"}

        for attr, value in data.items():
            if value in ALLOWED_FIELDS and value is not None:
                setattr(product, attr, value)

        await session.commit()
        await session.refresh(product)

        return product

    @staticmethod
    async def delete_product(session: AsyncSession, product: Product) -> None:
        await session.delete(product)
        await session.commit()
