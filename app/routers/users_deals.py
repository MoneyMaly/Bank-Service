from typing import Optional, List

from fastapi import APIRouter, HTTPException, status, Depends

from app.adapters.db_adapter import insert_users_deal, get_users_account
from app.utils.auth_helper import JWTBearer
from app.models import ExpenceorRevenue, Deal, UsersDeal

router = APIRouter(tags=['Users deals'])

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"})

account_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Users Bank Account doesn't exist",
    headers={"WWW-Authenticate": "Bearer"})

@router.post("/users/{username}/bankaccounts/{account_number}/deals",status_code=status.HTTP_200_OK, response_model_exclude=['_id'], dependencies=[Depends(JWTBearer())])
async def add_users_deal_info(username: str, account_number: str, deal_info: Deal):
    if JWTBearer.authenticated_username != username:
        raise credentials_exception
    account = await get_users_account(username, account_number)
    if account:
        deal_info = deal_info.__dict__
        deal_info["username"] = username
        deal_info["account_number"] = account_number
        users_deal =  UsersDeal(**deal_info)
        is_success = await insert_users_deal(users_deal)
        return is_success
    raise account_not_found_exception