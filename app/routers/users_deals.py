from typing import Optional, List

from fastapi import APIRouter, HTTPException, status, Depends

from app.adapters.db_adapter import upsert_user_deal, get_user_account, get_user_deals_list, delete_user_deal
from app.utils.auth_helper import JWTBearer
from app.models import ExpenceorRevenue, Deal, UserDeal

router = APIRouter(tags=['Users Deals'])

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"})

account_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Users Bank Account doesn't exist",
    headers={"WWW-Authenticate": "Bearer"})

@router.post("/users/{username}/bankaccounts/{account_number}/deals",status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def add_user_deal_info(username: str, account_number: str, deal_info: Deal):
    if JWTBearer.authenticated_username != username:
        raise credentials_exception
    account = await get_user_account(username, account_number)
    if account:
        deal_info = deal_info.__dict__
        deal_info["username"] = username
        deal_info["account_number"] = account_number
        user_deal =  UserDeal(**deal_info)
        is_success = await upsert_user_deal(user_deal)
        return is_success
    raise account_not_found_exception

@router.get("/users/{username}/bankaccounts/{account_number}/deals",status_code=status.HTTP_200_OK, response_model=List[UserDeal], dependencies=[Depends(JWTBearer())])
async def get_user_deals(username: str, account_number: str):
    if JWTBearer.authenticated_username != username:
        raise credentials_exception
    deals_list = await get_user_deals_list(username, account_number)
    return deals_list

@router.delete("/users/{username}/bankaccounts/{account_number}/deals/company/{company}",status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def remove_user_deal(username: str, account_number: str, company: str):
    if JWTBearer.authenticated_username != username:
        raise credentials_exception
    deleted_count = await delete_user_deal(username, account_number,company)
    return f"{deleted_count} deals successfully removed"