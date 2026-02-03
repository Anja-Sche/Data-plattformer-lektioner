from pydantic import BaseModel

from typing import Union

class ProductSchema(BaseModel):
    product_id: str
    name: str
    price: float
    currency: str # SEK, USD, EUR
    category: Union[str, None]
    brand: Union[str, None]  # TODO - Checkup the optional alternative
