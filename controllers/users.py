from abc import ABC
from utils.database import Database

class User(ABC):

  @staticmethod
  def get_users():
    query = "select name from sys.databases"
    res = Database.execute_query_json(query)
    return res