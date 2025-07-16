from fastapi import FastAPI
from controllers.products import Product

from models.userregistry import UserRegister
from models.loginuser import UserLogin
from controllers.firebase import Firebase

app = FastAPI()

@app.get('/')
def root():
  return { 'version': '0.1.0' }

@app.get('/products')
async def databases(limit: int = None, brand: str = None, color: str = None):
  res = await Product.get_products_with_filter(brand, color, limit) 
  return res

@app.post('/signup')
async def signup(user: UserRegister):
  res = await Firebase.signup(user)
  return res

@app.post('/login')
async def login(user: UserLogin):
  res = await Firebase.login_user_firebase(user)
  return res