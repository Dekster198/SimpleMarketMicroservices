from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from models import UserRole


class UserBase(BaseModel):
    email: EmailStr
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: UserRole

    name: str = Field(min_length=2, max_length=50)
    phone: str = Field(min_length=11, max_length=11)


class UserUpdate(BaseModel):
    email: str | None = None
    role: UserRole | None = None


class UserPublic(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole


class SellerBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    phone: str = Field(min_length=11, max_length=11)
    rating: float

    model_config = ConfigDict(from_attributes=True)


class SellerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    phone: str = Field(min_length=11, max_length=11)


class SellerUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None


class SellerPublic(BaseModel):
    id: UUID
    name: str
    phone: str
    rating: float


class BuyerBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    phone: str = Field(min_length=11, max_length=11)

    model_config = ConfigDict(from_attributes=True)


class BuyerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    phone: str = Field(min_length=11, max_length=11)


class BuyerUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None


class BuyerPublic(BaseModel):
    id: UUID
    name: str
    phone: str
