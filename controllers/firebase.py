from fastapi import HTTPException
from dotenv import load_dotenv
import logging
import os
import requests
from abc import ABC
import firebase_admin
from firebase_admin import credentials, auth

from models.userregistry import UserRegister
from models.loginuser import UserLogin
from utils.database import Database
from utils.auth_token import JWT

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cred = credentials.Certificate("secrets/secrets.json")
firebase_admin.initialize_app(cred)

load_dotenv()

class Firebase(ABC):

  @staticmethod
  async def signup(user: UserRegister) -> dict:
    user_record = {}
    try:
      user_record = auth.create_user(email=user.email, password=user.password) 
    except Exception as e:
      logger.error(f'could not create user in firebase {e}')
      raise HTTPException(status_code=400, detail=f"error while creating user {e}")
    
    query = "INSERT INTO redis.Users (email, first_name, last_name, active, admin) VALUES (?, ?, ?, ?, ?)"
    params = [user_record.email, user.first_name, user.last_name, user.active, user.admin]

    try:
      res = await Database.execute_query_json(query, params, needs_commit=True)
      return res
    except Exception as e:
      logger.error(f'error while inserting user to database... {e}')
      raise HTTPException(status_code=500, detail=f'error while creating user... {e}') 

  @staticmethod
  async def login_user_firebase(user: UserLogin):
      api_key = os.getenv("FIREBASE_API_KEY")
      url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
      payload = {
          "email": user.email,
          "password": user.password,
          "returnSecureToken": True
      }
      response = requests.post(url, json=payload)
      response_data = response.json()

      if "error" in response_data:
          raise HTTPException(
              status_code=400,
              detail=f"Error al autenticar usuario: {response_data['error']['message']}"
          )

      query = f"select email,first_name,last_name,active,admin from redis.Users where email = ?"
      params = [user.email]

      try:
          result = await Database.execute_query_json(query, params, needs_commit=False)
          logger.info(f'USER: {result[0]}')
          token = JWT.create_jwt_token(result[0])
          logger.info(f'TOKEN: {token}')
          return {
              "message": "Usuario autenticado exitosamente",
              "idToken": token 
          }
      except Exception as e:
          raise HTTPException(status_code=500, detail=str(e))