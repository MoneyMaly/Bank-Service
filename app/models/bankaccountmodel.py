from typing import Optional
from pydantic import BaseModel, Field
from app.utils.db_helper import PyObjectId


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