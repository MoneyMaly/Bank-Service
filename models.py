from typing import Optional
from pydantic import BaseModel, Field
from app.utils.db_helper import PyObjectId
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class UserBankAccount(BaseModel):
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
    date: datetime

class Deal(BaseModel):
    company: str
    # can be Communication, TV, insurance
    sector: str
    extra_info: dict

class UserDeal(Deal):
    username: str
    account_number: str
class CompanyMonthlyPrice(BaseModel):
    company: str
    price: int
    year: int
    month: int 
    date: datetime