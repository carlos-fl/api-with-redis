from pydantic import BaseModel

class Product(BaseModel):
  product_id: str
  product_name: str
  product_brand: str
  gender: str
  price: float
  num_images: int
  description: str
  primary_color: str
