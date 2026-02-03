from pydantic import BaseModel

from typing import Union

class DimensionsSchema(BaseModel):
    width_cm: float
    height_cm: float
    depth_cm: float

class ProductSchema(BaseModel):
    product_id: str
    name: str
    price: float
    currency: str # SEK, USD, EUR
    category: Union[str, None]
    brand: Union[str, None]
    tags: Union[list[str],None]
    dimensions: Union[DimensionsSchema, None]
