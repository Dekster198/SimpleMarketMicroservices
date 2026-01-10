import decimal
from typing import Optional

from sqlalchemy import Numeric
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
    seller_id: Mapped[int] = mapped_column(index=True, nullable=False)
