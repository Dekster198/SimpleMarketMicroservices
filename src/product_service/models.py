import decimal
from datetime import datetime
from typing import Optional

from sqlalchemy import Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    price: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    rating: Mapped[float] = mapped_column(default=0.0, nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    reserved_quantity: Mapped[int] = mapped_column(default=0)
    seller_id: Mapped[int] = mapped_column(index=True, nullable=False)


class ProductReservation(Base):
    __tablename__ = 'product_reservation'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(index=True, nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime]

    __table_args__ = (
        UniqueConstraint("order_id", "product_id", name="uq_order_product"),
    )
