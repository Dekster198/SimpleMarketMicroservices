import decimal

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price: decimal.Decimal = Field(gt=0)
    quantity: int = Field(ge=0)


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
