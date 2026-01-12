import decimal
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field
from typing_extensions import Self


class ProductBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price: decimal.Decimal = Field(..., gt=0)
    quantity: int = Field(..., ge=0)


class ProductCreate(ProductBase):
    seller_id: int


class ProductUpdate(BaseModel):
    title: str | None = Field(None, min_length=2, max_length=500)
    description: str | None = Field(None, max_length=500)
    price: decimal.Decimal | None = Field(None, gt=0)
    quantity: int | None = Field(None, ge=0)


class ProductPublic(ProductBase):
    id: int
    rating: float
    seller_id: int

    class Config:
        from_attributes = True


class ReserveItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class ProductReserveRequest(BaseModel):  # вызывает OrderService при создании заказа
    order_id: int = Field(..., gt=0)
    items: list[ReserveItem]  # items = [{'product_id': 1, 'quantity': 5}, {'product_id': 2, 'quantity': 20}]

    @classmethod
    def validate_items_not_empty(cls, values):
        if not values.get('items'):
            raise ValueError('Items list cannot be empty')
        return values


class ProductReserveResponse(BaseModel):
    product_id: int


class ProductReleaseRequest(BaseModel):
    order_id: int = Field(..., gt=0)


class ProductCommitRequest(BaseModel):
    order_id: int = Field(..., gt=0)


class ReservationStatus(Enum):
    RESERVED = 'reserved'
    RELEASED = 'released'
    COMMITED = 'commited'


class ReservationStatusResponse(BaseModel):
    status: ReservationStatus
