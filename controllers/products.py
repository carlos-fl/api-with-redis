from abc import ABC
import logging
from utils.database import Database
from models.product import ProductModel
from utils.redis_cache import Redis

CACHE_TTL = 1800
BASE_CACHE_KEY = 'products:catalog'

logger = logging.getLogger(__name__)

class Product(ABC):

  @staticmethod
  def get_products_limit(limit: int) -> list[ProductModel]:
    query = "select top ? * from redis.Products"
    params = [limit]
    res = Database.execute_query_json(query, params)
    return res
  
  @staticmethod
  def get_all_products() -> list[ProductModel]:
    query = "select * from redis.Products"
    res = Database.execute_query_json(query)
    return res

  
  @staticmethod
  async def get_products_with_filter(brand: str, color: str) -> list[ProductModel]:
    key = ''
    if not brand and not color:
      key = 'all'
    else:
      key = f'brand={brand}:color={color}'

    redis_client = Redis.get_redis_client()
    cached_data = Redis.get_from_cache(redis_client, f'{BASE_CACHE_KEY}:{key}')
    logger.info(f'GENERATED KEY FOR REDIS: {BASE_CACHE_KEY}:{key}')

    if cached_data:
      logging.info('Data was retrieved by REDIS')
      return cached_data 

    base_query = 'SELECT * FROM redis.Products'
    params = []
    
    where_sentence = []
    if brand:
      where_sentence.append("ProductBrand like ?")
      params.append(brand)
    if color:
      where_sentence.append("PrimaryColor like ?")
      params.append(f"%{color}%")
    if where_sentence:
      base_query += " WHERE " + " AND ".join(where_sentence)
    
    res = await Database.execute_query_json(base_query, params)
    logging.info(f'type of res: {type(res)}')
    Redis.store_in_cache(redis_client, f'{BASE_CACHE_KEY}:{key}', res, CACHE_TTL)
    logging.info('Data was retrieved by DATABASE')
    return res
  
  @staticmethod
  async def create_product(product: ProductModel) -> dict:
    query = 'INSERT INTO redis.Products (ProductID, ProductName, ProductBrand, Gender, Price, NumImages, Description, PrimaryColor) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
    params = [
      product.ProductID, 
      product.ProductName, 
      product.ProductBrand, 
      product.Gender, 
      product.Price, 
      product.NumImages, 
      product.Description, 
      product.PrimaryColor
      ]

    await Database.execute_query_json(query, params, needs_commit=True)
    REDIS_KEYS = [f'{BASE_CACHE_KEY}:all',
                  f'{BASE_CACHE_KEY}:brand={product.ProductBrand}:color={product.PrimaryColor}',
                  f'{BASE_CACHE_KEY}:brand=None:color={product.PrimaryColor}',
                  f'{BASE_CACHE_KEY}:brand={product.ProductBrand}:color=None',
                  ]
    redis_client = Redis.get_redis_client()
    for key in REDIS_KEYS:
      was_cache_deleted = Redis.delete_cache(redis_client, f'{key}')
      logger.info(f'KEY {key} was attempted to be deleted. Output: {was_cache_deleted}')
    
    return { 'success': True }

