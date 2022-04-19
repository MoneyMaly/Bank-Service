from typing import Optional, List

from fastapi import APIRouter, HTTPException, status, Depends

from app.adapters.db_adapter import get_bank_accounts_list_by_username, get_monthly_balance, create_user_bank_account
from app.utils.auth_helper import JWTBearer
from app.models import BankAccountByUsername, BankAccountBalance, ExpenceorRevenue

router = APIRouter(tags=['Bank'])

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"})


@router.get("/users/{username}/bankaccounts/",status_code=status.HTTP_200_OK,response_model=List[BankAccountByUsername], 
response_model_exclude=['_id'], dependencies=[Depends(JWTBearer())])
async def get_bank_accounts_list(username: str):
    if JWTBearer.authenticated_username != username:
        raise credentials_exception
    bank_accounts_list = await get_bank_accounts_list_by_username(username)
    return bank_accounts_list

@router.post("/users/{username}/bankaccounts/",status_code=status.HTTP_200_OK, response_model_exclude=['_id'], dependencies=[Depends(JWTBearer())])
async def get_bank_accounts_list(bank_account: BankAccountByUsername):
    if JWTBearer.authenticated_username != bank_account.username:
        raise credentials_exception
    bank_accounts_list = await create_user_bank_account(bank_account)
    return bank_accounts_list

@router.get("/users/{username}/bankaccounts/balance/",status_code=status.HTTP_200_OK,response_model=List[ExpenceorRevenue], response_model_exclude=['id'], dependencies=[Depends(JWTBearer())])
async def get_monthly_balance_by_user(username: str, month: Optional[int] = 1, year: Optional[int] = 2020):
    if JWTBearer.authenticated_username != username:
        raise credentials_exception
    bank_accounts_list = await get_bank_accounts_list_by_username(username)
    monthly_balance = await get_monthly_balance(bank_accounts_list, year, month)
    return monthly_balance
#     monthly_balance = get_monthly_balance(bank_accounts_list, year, month)
#     return [{"owner": username, "year": year, "month": month, "monthly_balance": monthly_balance}]

#TO DO get balance for specific account 