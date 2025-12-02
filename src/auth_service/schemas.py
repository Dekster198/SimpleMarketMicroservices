from uuid import UUID
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

from src.auth_service.models import UserRole


class UserSchema(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole


class UserUpdate(BaseModel):
    email: str | None = None
    role: UserRole | None = None


class UserPublic(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole


class SellerSchema(BaseModel):
    id: UUID
    name: str
    phone: str
    rating: float

    model_config = ConfigDict(from_attributes=True)


class SellerCreate(BaseModel):
    name: str
    phone: str


class SellerUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None


class SellerPublic(BaseModel):
    id: UUID
    name: str
    phone: str
    rating: float


class BuyerSchema(BaseModel):
    id: UUID
    name: str
    phone: str

    model_config = ConfigDict(from_attributes=True)


class BuyerCreate(BaseModel):
    name: str
    phone: str


class BuyerUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None


class BuyerPublic(BaseModel):
    id: UUID
    name: str
    phone: str
