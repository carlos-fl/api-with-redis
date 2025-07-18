from abc import ABC
from utils.database import Database

class User(ABC):
  @staticmethod
  async def get_users() -> list:
    query = "SELECT * FROM redis.Users"
    res = await Database.execute_query_json(query)
    return res