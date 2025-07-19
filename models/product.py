from pydantic import BaseModel

class ProductModel(BaseModel):
  ProductID: int
  ProductName: str
  ProductBrand: str
  Gender: str
  Price: float
  NumImages: int
  Description: str
  PrimaryColor: str
