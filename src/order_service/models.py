from decimal import Decimal
from enum import Enum
from datetime import datetime
from sqlalchemy import text, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class OrderStatus(Enum):
    NEW = 'new'
    RESERVING = 'reserving'
    RESERVED = 'reserved'
    PAID = 'paid'
    CANCELED = 'canceled'


class OrderItemStatus(str, Enum):
    PENDING = "pending"
    RESERVED = "reserved"
    FAILED = "failed"


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    buyer_id: Mapped[int]
    status: Mapped[Enum] = mapped_column(default=OrderStatus.NEW)
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    items = relationship('OrderItem', back_populates='order')


class OrderItem(Base):
    __tablename__ = 'order_item'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    product_id: Mapped[int]
    seller_id: Mapped[int]
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    quantity: Mapped[int]

    order = relationship('Order', back_populates='items')
