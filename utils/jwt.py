import os
from datetime import datetime, timedelta
from abc import ABC
import jwt
from dotenv import load_dotenv

from models.userregistry import UserRegister

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

class JWT(ABC):

  @staticmethod
  def create_jwt_token(user: UserRegister):
    expiration = datetime.now() + timedelta(hours=1) 
    token = jwt.encode(
        {
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "active": user.active,
            "admin": user.admin,
            "exp": expiration,
            "iat": datetime.now()
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    return token
