from typing import Optional

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    price: str


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[str] = None


class ProductModel(BaseModel):
    id: int
    name: str
    description: str
    price: str

    class Config:
        from_attributes = True
