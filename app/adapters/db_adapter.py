from pymongo import MongoClient
from uuid import uuid4
from bson import ObjectId

from app.models import BankAccountBalance, UserBankAccount, UserDeal
from app.settings import DATABASE_SERVER, DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT, DATABASE_NAME

client = None
db = None

async def get_bank_accounts_list_by_username(username: str):
    bank_accounts = await db["UsersBankAccounts"].find({"username":username}).to_list(length=5)
    return list(bank_accounts)
# UsersBankAccounts
async def create_user_bank_account(bank_account: UserBankAccount):
    try:
        res = await db["UsersBankAccounts"].insert_one(bank_account.__dict__)
        return True
    except:
        return False

async def delete_user_bank_account(username: str, account_number: str):
    res = await db["UsersBankAccounts"].delete_one({"username": username, "account_number": account_number})
    return res.deleted_count

async def get_user_account(username: str, account_number: str):
    user_account = await db["UsersBankAccounts"].find_one({"username": username, "account_number": account_number})
    return user_account

# BankAccounts   
async def get_account_monthly_balance(bank_account, year: int, month: int):
    account_monthly_balance = await db["BankAccounts"].find_one({"owner": bank_account["owner"], \
    "ssn": bank_account["ssn"], "account_number":bank_account["account_number"], "year": year, "month": month})
    return account_monthly_balance

async def get_account_monthly_balance_by_number(account_number: str,year : int, month: int):
    account_monthly_balance = await db["BankAccounts"].find_one({"account_number": account_number, "year": year, "month": month})
    return account_monthly_balance
# UsersDeals
async def upsert_user_deal(user_deal: UserDeal):
    try:
        res = await db["UsersDeals"].update_one({"username": user_deal.username, "account_number": user_deal.account_number, "company": user_deal.company},
        {"$set":user_deal.__dict__},upsert=True)
        return True
    except:
        return False

async def delete_user_deal(username: str, account_number: str, company: str):
    res = await db["UsersDeals"].delete_one({"username": username, "account_number": account_number, "company": company})
    return res.deleted_count

async def get_user_deals_list(username: str, account_number: str):
    user_deals = await db["UsersDeals"].find({"username": username, "account_number": account_number}).to_list(length=10)
    return list(user_deals)

async def get_deals_list(sector : str):
    user_deals = await db["UsersDeals"].find({"sector": sector}).to_list(length=50)
    return list(user_deals)

async def get_deal_by_id(id : str):
    deal = await db["UsersDeals"].find_one({"_id": ObjectId(id)})
    return deal 