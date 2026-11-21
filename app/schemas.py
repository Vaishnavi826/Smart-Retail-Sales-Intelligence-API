
from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProductCreate(BaseModel):
    stock_code: str
    description: Optional[str] = None


class ProductUpdate(BaseModel):
    stock_code: Optional[str] = None
    description: Optional[str] = None


class ProductResponse(BaseModel):
    product_id: int
    stock_code: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
