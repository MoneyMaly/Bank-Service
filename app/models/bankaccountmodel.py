from typing import Optional
from pydantic import BaseModel, Field
from app.utils.db_helper import PyObjectId


class BankAccountByUsername(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    username: str
    ssn: str
    owner: str
    account_number:str

class BankAccountBalance(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    ssn: str
    owner: str
    account_number:str
    year: int
    month: int
    expenses_and_revenues: list 