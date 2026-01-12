from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.product_service.models import Product, ProductReservation


class ProductReservationService:
    @staticmethod
    async def reserve(
            session: AsyncSession,
            order_id: int,
            product_id: int,
            quantity: int
    ) -> None:
        stmt = select(ProductReservation).where(
            ProductReservation.order_id == order_id,
            ProductReservation.product_id == product_id
        )
        result = await session.execute(stmt)
        if result.scalar_one_or_none():
            return

        product = await session.get(Product, product_id)
        if not product:
            raise ValueError('Product not found')

        available = product.quantity - quantity

        if available < quantity:
            raise ValueError('Not enough product quantity')

        product.reserved_quantity += quantity

        reservation = ProductReservation(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity
        )
        session.add(reservation)

        await session.commit()

    @staticmethod
    async def release(
            session: AsyncSession,
            order_id: int
    ) -> None:
        stmt = select(ProductReservation).where(ProductReservation.order_id == order_id)
        result = await session.execute(stmt)
        reservations = result.scalars().all()

        if not reservations:
            return

        for r in reservations:
            product = await session.get(Product, r.product_id)
            product.reserved_quantity -= r.quantity
            await session.delete(r)

        await session.commit()

    @staticmethod
    async def commit(
            session: AsyncSession,
            order_id: int
    ) -> None:
        stmt = select(ProductReservation).where(ProductReservation.order_id == order_id)
        result = await session.execute(stmt)
        reservations = result.scalars().all()

        if not reservations:
            return

        for r in reservations:
            product = await session.get(Product, r.product_id)
            product.quantity -= r.quantity
            product.reserved_quantity -= r.quantity
            await session.delete(r)

        await session.commit()

