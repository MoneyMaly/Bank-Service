import uvicorn
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.routers import bank
from app.consts import DEFAULT_PREFIX, TOKEN_SECTION, BANK_SECTION

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

@app.get('/')
async def index():
  return {'hello': 'world'}

# routers
app.include_router(bank.router, prefix=DEFAULT_PREFIX, tags=[BANK_SECTION])


if __name__ == '__main__':  # For Debugging
    uvicorn.run(app, host='0.0.0.0', port=5000)