from calendar import month
from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends

from app.adapters.db_adapter import upsert_user_deal, get_user_account, get_user_deals_list, delete_user_deal, get_deals_list, get_deal_by_id
from app.utils.auth_helper import JWTBearer
from app.models import ExpenceorRevenue, Deal, UserDeal, DealDetails
from app.routers.bank import get_company_price

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

@router.get("/users/{username}/bankaccounts/{account_number}/deals",status_code=status.HTTP_200_OK, response_model=List[UserDeal], response_model_exclude=['id'], dependencies=[Depends(JWTBearer())])
async def get_user_deals(username: str, account_number: str):
    if JWTBearer.authenticated_username != username:
        raise credentials_exception
    deals_list = await get_user_deals_list(username, account_number)
    return deals_list

@router.delete("/users/{username}/bankaccounts/{account_number}/deals/company/{company}",status_code=status.HTTP_200_OK, response_model_exclude=['id'], dependencies=[Depends(JWTBearer())])
async def remove_user_deal(username: str, account_number: str, company: str):
    if JWTBearer.authenticated_username != username:
        raise credentials_exception
    deleted_count = await delete_user_deal(username, account_number,company)
    return f"{deleted_count} deals successfully removed"

@router.get("/deals/sectors/{sector}",status_code=status.HTTP_200_OK, response_model=List[DealDetails], response_model_exclude=['username', 'account_number'], dependencies=[Depends(JWTBearer())])
async def get_deals_full_details_anonymously(sector: str):
    today = datetime.today()
    deals_list = await get_deals_list(sector)
    current_list = []
    for deal in deals_list:
        deal_details= await get_company_price(account_number=deal['account_number'], company=deal['company'], month=today.month, year=today.year)
        if deal_details:
            deal['price']= deal_details['price']
            current_list.append(deal)
    return current_list

@router.get("/deals/deal_id/{id}",status_code=status.HTTP_200_OK, response_model=UserDeal, dependencies=[Depends(JWTBearer())])
async def get_deal_from_id(id: str):
    if JWTBearer.role != "business":
        raise credentials_exception
    deal = await get_deal_by_id(id)
    return deal 