from typing import Optional, List

from fastapi import APIRouter, HTTPException, status, Depends

from app.adapters.db_adapter import get_bank_accounts_list_by_username, create_user_bank_account, delete_user_bank_account
from app.utils.auth_helper import JWTBearer
from app.models import UserBankAccount, BankAccountBalance, ExpenceorRevenue

router = APIRouter(tags=['Users Bank Accounts'])

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"})


@router.get("/users/{username}/bankaccounts/",status_code=status.HTTP_200_OK, response_model=List[UserBankAccount], dependencies=[Depends(JWTBearer())])
async def get_bank_accounts_list(username: str):
    if JWTBearer.authenticated_username != username:
        raise credentials_exception
    bank_accounts_list = await get_bank_accounts_list_by_username(username)
    return bank_accounts_list

@router.post("/users/{username}/bankaccounts/",status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def add_bank_accounts_list(bank_account: UserBankAccount):
    if JWTBearer.authenticated_username != bank_account.username:
        raise credentials_exception
    success = await create_user_bank_account(bank_account)
    return success

@router.delete("/users/{username}/bankaccounts/{account_number}/",status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def remove_user_bank_account(username: str, account_number: str):
    if JWTBearer.authenticated_username != username:
        raise credentials_exception
    deleted_count = await delete_user_bank_account(username, account_number)
    return f"{deleted_count} accounts successfully removed"
