from abc import ABC
import os
import orjson
import logging
import redis
from dotenv import load_dotenv

from models.product import ProductModel

load_dotenv()

logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_STRING")

class Redis(ABC):
  @staticmethod
  def get_redis_client():
      if not REDIS_URL:
          logger.error("La variable de entorno REDIS_STRING no está definida.")
          return None

      try:
          client = redis.Redis.from_url(
              REDIS_URL,
              decode_responses=True
          )

          client.ping()
          logger.info("Connected to Redis successfully using Connection String!")
          return client
      except Exception as e:
          logger.error(f"Error connecting to Redis with Connection String: {e}")
          logger.error(f'REDIS_URL: {REDIS_URL}')
          return None

  @staticmethod
  def get_from_cache(redis_client, cache_key: str) -> list:
      if not redis_client:
          return None

      try:
          cached_data = redis_client.get(cache_key)
          if cached_data:
              logger.info(f"Cache found for key: {cache_key}")
              return orjson.loads(cached_data)
      except orjson.JSONDecodeError as e:
          logger.warning(f"Corrupted cache data for key {cache_key}, error: {str(e)}")
          redis_client.delete(cache_key)
      except Exception as e:
          logger.warning(f"Cache retrieval failed for key '{cache_key}': {str(e)}")

      return None


  def delete_cache(redis_client, cache_key: str) -> bool:
      if not redis_client:
          logger.info("Redis not available - cache deletion skipped")
          return False

      try:
          result = redis_client.delete(cache_key)
          if result:
              logger.info(f"Cache key '{cache_key}' deleted successfully")
              return True
          else:
              logger.info(f"Cache key '{cache_key}' did not exist")
              return False
      except Exception as e:
          logger.warning(f"Failed to delete cache key '{cache_key}': {str(e)}")
          return False


  def store_in_cache(redis_client, cache_key: str, data: list[ProductModel], expiration: int) -> None:
      if not redis_client:
          logger.info("Redis not available - running without cache")
          return

      try:
          json_data = orjson.dumps(data, default=str)
          redis_client.setex(cache_key, expiration, json_data)
          logger.info(f"products catalog cached for {expiration} seconds")
      except Exception as e:
          logger.warning(f"Failed to cache series catalog: {str(e)}")