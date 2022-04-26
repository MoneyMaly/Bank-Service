from typing import Optional, List

from fastapi import APIRouter, HTTPException, status, Depends

from app.adapters.db_adapter import get_bank_accounts_list_by_username, get_account_monthly_balance, get_account_monthly_balance_by_number
from app.utils.auth_helper import JWTBearer
from app.models import UserBankAccount, BankAccountBalance, ExpenceorRevenue, CompanyMonthlyPrice

router = APIRouter(tags=['Banking Service'])

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"})

async def get_company_price(account_number: str, company: str, year: int, month: int):
    company_payment = {}
    monthly_balance = await get_account_monthly_balance_by_number(account_number, year, month)
    if monthly_balance:
        company_pay = next((pay for pay in monthly_balance['expenses_and_revenues'] if pay['subject'] == company), None)
        company_payment['company'] = company
        company_payment['year'] = year
        company_payment['month'] = month
        if company_payment and company_pay:
            company_payment['date'] = company_pay['date']
            company_payment['price'] = company_pay['price']
            return company_payment

@router.get("/users/{username}/bankaccounts/balance",status_code=status.HTTP_200_OK,response_model=List[ExpenceorRevenue], response_model_exclude=['id'], dependencies=[Depends(JWTBearer())])
async def get_user_monthly_balance(username: str, month: Optional[int] = 1, year: Optional[int] = 2022):
    if JWTBearer.authenticated_username != username:
        raise credentials_exception
    bank_accounts_list = await get_bank_accounts_list_by_username(username)
    total_monthly_balance_list = []
    for bank_account in bank_accounts_list:
        account_monthly_balance = await get_account_monthly_balance(bank_account, year, month)
        if account_monthly_balance is not None:
            total_monthly_balance_list += account_monthly_balance['expenses_and_revenues']
    return total_monthly_balance_list

@router.get("/users/{username}/bankaccounts/{account_number}",status_code=status.HTTP_200_OK,response_model=List[ExpenceorRevenue], response_model_exclude=['id'], dependencies=[Depends(JWTBearer())])
async def get_account_monthly_balance_by_user(username: str, account_number: str, ssn: str, owner: str, month: Optional[int] = 1, year: Optional[int] = 2022):
    if JWTBearer.authenticated_username != username:
        raise credentials_exception
    user_bank_account = {}
    bank_account_properties = ["username","account_number","ssn","owner"]
    for prop in bank_account_properties:
        user_bank_account[prop] = eval(prop)
    bank_account = await  get_account_monthly_balance(user_bank_account, year, month)
    if bank_account is not None:
        return bank_account['expenses_and_revenues']
    return []

@router.get("/users/{username}/bankaccounts/{account_number}/company/{company}",status_code=status.HTTP_200_OK,response_model=CompanyMonthlyPrice, response_model_exclude=['id'], dependencies=[Depends(JWTBearer())])
async def get_company_monthly_price(username: str, account_number: str, company: str, month: Optional[int] = 1, year: Optional[int] = 2020):
    if JWTBearer.authenticated_username != username:
        raise credentials_exception
    company_payment = await get_company_price(account_number=account_number, company= company, year= year, month= month)
    return company_payment