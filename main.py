from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
import logging

from controllers.products import Product
from controllers.users import User

from models.userregistry import UserRegister
from models.product import ProductModel
from models.loginuser import UserLogin
from controllers.firebase import Firebase

from utils.authorization_decorators import admin
from utils.insights import setup_simple_telemetry, instrument_fastapi_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

telemetry_enabled = setup_simple_telemetry()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting API...")
    yield
    logger.info("Shutting down API...")


app = FastAPI(
  title='PRODUCTS API',
  description='this is a simple api with redis implementation',
  lifespan=lifespan
)

if telemetry_enabled:
  instrument_fastapi_app(app)
  logger.info('fast api insights enabled')
  logger.info('fast api instrumented')
else:
  logger.warning('insights disabled')

# Products endpoints
@app.get('/')
def root():
  return { 
    'version': '0.1.0',
    'description': 'Ecommerce clothes Products'
    }

@app.get('/products')
async def get_products(brand: str = None, color: str = None):
  res = await Product.get_products_with_filter(brand, color) 
  return res

@app.post('/products')
@admin
async def create_product(request: Request, product: ProductModel):
  res = await Product.create_product(product) 
  return res


# User endpoints
@app.post('/signup')
async def signup(user: UserRegister):
  res = await Firebase.signup(user)
  return res

@app.post('/login')
async def login(user: UserLogin):
  res = await Firebase.login_user_firebase(user)
  return res

@app.get('/users')
@admin
async def get_users(request: Request) -> list:
  res = await User.get_users()
  return res