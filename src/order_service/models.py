import decimal
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    buyer_id: Mapped[int]
    total_price: Mapped[decimal]
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


class OrderItem(Base):
    __tablename__ = 'order_item'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int]
    product_id: Mapped[int]
    seller_id: Mapped[int]
    price: Mapped[decimal]
    quantity: Mapped[int]
