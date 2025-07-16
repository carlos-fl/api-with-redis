from abc import ABC
from utils.database import Database
from models.product import Product

class Product(ABC):

  @staticmethod
  def get_products_limit(limit: int) -> list[Product]:
    query = "select top ? * from redis.Products"
    params = [limit]
    res = Database.execute_query_json(query, params)
    return res
  
  @staticmethod
  def get_all_products() -> list[Product]:
    query = "select * from redis.Products"
    res = Database.execute_query_json(query)
    return res

  
  @staticmethod
  def get_products_with_filter(brand: str, color: str, limit: int) -> list[Product]:
    base_query = 'SELECT'
    params = []

    if limit:
      base_query += f" TOP {limit} *"
    else:
      base_query += f" *"
    
    base_query += " FROM redis.Products"
    
    where_sentence = []
    if brand:
      where_sentence.append("ProductBrand like ?")
      params.append(brand)
    if color:
      where_sentence.append("PrimaryColor like ?")
      params.append(f"%{color}%")
    if where_sentence:
      base_query += " WHERE " + " AND ".join(where_sentence)
    
    res = Database.execute_query_json(base_query, params)
    return res

