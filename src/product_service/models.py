import decimal
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[decimal]
    rating: Mapped[float]
    quantity: Mapped[int]
    seller_id: Mapped[int]
