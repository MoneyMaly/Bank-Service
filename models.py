from typing import Optional
from pydantic import BaseModel, Field
from app.utils.db_helper import PyObjectId

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class BankAccountByUsername(BaseModel):
    username: Optional[str] = None
    owner: Optional[str] = None
    ssn: Optional[str] = None
    account_number: Optional[str] = None
class BankAccountBalance(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    ssn: str
    owner: str
    account_number:str
    year: int
    month: int
    expenses_and_revenues: list

class ExpenceorRevenue(BaseModel):
    price: str
    subject:str 