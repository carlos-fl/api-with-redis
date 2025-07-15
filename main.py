from fastapi import FastAPI
from controllers.users import User

app = FastAPI()

@app.get('/')
def root():
  return { 'version': '0.1.0' }


@app.get('/testing')
async def databases():
  res = await User.get_users()
  return res
