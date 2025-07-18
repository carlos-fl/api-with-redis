import os
from datetime import datetime, timedelta
from abc import ABC
import jwt
import logging
from dotenv import load_dotenv

from models.userregistry import UserRegister

# configurar loggin
logging.basicConfig(level=logging.INFO, format=f'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

class JWT(ABC):

  @staticmethod
  def create_jwt_token(user: UserRegister):
    expiration = datetime.utcnow() + timedelta(hours=1) 
    payload = {
            "firstname": user['first_name'],
            "lastname": user['last_name'],
            "email": user['email'],
            "active": user['active'],
            "admin": user['admin'],
            "exp": expiration,
            "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token
