from abc import ABC
import os
from dotenv import load_dotenv
import logging
import pyodbc
import json


load_dotenv()

DB_DRIVER = os.getenv('DB_DRIVER') 
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_SERVER = os.getenv('DB_SERVER')
DB_PORT = 1433
DB_USER = os.getenv('DB_USER')
DB_NAME = os.getenv('DB_NAME')



# configurar loggin
logging.basicConfig(level=logging.INFO, format=f'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

conn_str = (
    f"DRIVER={DB_DRIVER};"
    f"SERVER={DB_SERVER},{DB_PORT};"
    f"DATABASE={DB_NAME};"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)

class Database(ABC):

  _instance = None

  @staticmethod
  async def get_instace():
    if Database._instance is None:
      try:
        conn = pyodbc.connect(conn_str, timeout=10)
        logger.info('Connected to database successful')
        _instance = conn
        return _instance
      except pyodbc.Error as e:
        logger.error(f'Error while trying to connect to database. {str(e)}')
        logger.error(f'string connection: {conn_str}')
        raise Exception(f'Error while trying to connect to database. {str(e)}')

      except Exception as e:
        logger.error(f'Error while trying to connect to database. {str(e)}')
        raise Exception(f'Error while trying to connect to database. {str(e)}')

    else:
      return Database._instance

  
  @staticmethod
  async def execute_query_json(sql_template, params=None, needs_commit=False):
    conn = cursor = None
    try:
      conn = await Database.get_instace()
      cursor = conn.cursor()
      param_info = '(no parameters)' if not params else f'(with {len(params)} params)'
      logger.info(f'executing query with {param_info} : {sql_template}')

      if params:
        cursor.execute(sql_template, params)
      else:
        cursor.execute(sql_template)
      
      results = []
      if cursor.description:
        columns = [column[0] for column in cursor.description]
        logger.info(f'columns: {columns}')

        for row in cursor.fetchall():
          processed_row = [str(item) if isinstance(item, (bytes, bytearray)) else item for item in row]
          results.append(dict(zip(columns, processed_row)))
      
      else:
        logger.info('query did not return columns. possibly was not a SELECT query.')

      if needs_commit:
        logger.info('committing query...')
        conn.commit()
      
      return results

    except pyodbc.Error as e:
      logger.error(f'Error while trying to execute sql query {str(e)}') 
      if conn and needs_commit:
        try:
          logger.warning('Rollback...')
          conn.rollback()
        except pyodbc.Error as rb_e:
          logger.error(f'Error while trying rollback: {str(rb_e)}')
      raise Exception('Error while executing query')
    
    except Exception as e:
      logger.error(f'Error: {str(e)}')
      raise # raise an error
    
    finally:
      if cursor:
        cursor.close()
      if conn:
        conn.close()
        logger.info('Connection was closed')

