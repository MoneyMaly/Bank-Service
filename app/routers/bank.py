from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends

from app.adapters.db_adapter import get_bank_accounts_list_by_username, get_monthly_balance
from app.utils.auth_helper import get_current_user

router = APIRouter()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"})


@router.get("/users/{username}/bankaccounts/")
async def get_bank_accounts_list(authenticated_username: str = Depends(get_current_user), username=None):
    if authenticated_username != username:
        raise credentials_exception
    bank_accounts_list = get_bank_accounts_list_by_username(username)
    return [{"owner": username, "accounts_list": bank_accounts_list}]

@router.get("/users/{username}/bankaccounts/balance/")
async def get_monthly_balance_by_user(authenticated_username: str = Depends(get_current_user), username=None, month: Optional[int] = 1, year: Optional[int] = 2020):
    if authenticated_username != username:
        raise credentials_exception
    bank_accounts_list = get_bank_accounts_list_by_username(username)
    monthly_balance = get_monthly_balance(bank_accounts_list, year, month)
    return [{"owner": username, "year": year, "month": month, "monthly_balance": monthly_balance}]


#TO DO get balance for specific account 