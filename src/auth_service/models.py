import uuid
import enum
from datetime import datetime
from sqlalchemy import text, String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class UserRole(enum.Enum):
    seller = 'seller'
    buyer = 'buyer'
    admin = 'admin'


class User(Base):
    __tablename__ = 'user'

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(256))
    role: Mapped[UserRole]
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    seller: Mapped['Seller'] = relationship(back_populates='user', uselist=False, foreign_keys='Seller.id')
    buyer: Mapped['Buyer'] = relationship(back_populates='user', uselist=False, foreign_keys='Buyer.id')


class Seller(Base):
    __tablename__ = 'seller'

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id'), primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    phone: Mapped[str] = mapped_column(String(30))
    rating: Mapped[float] = mapped_column(Float, default=0.0)

    user: Mapped['User'] = relationship(back_populates='seller', foreign_keys=[id])


class Buyer(Base):
    __tablename__ = 'buyer'

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id'), primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    phone: Mapped[str] = mapped_column(String(30))

    user: Mapped['User'] = relationship(back_populates='buyer', foreign_keys=[id])
