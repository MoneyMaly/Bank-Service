from pymongo import MongoClient
from uuid import uuid4

from app.models import BankAccountBalance, UsersBankAccount, UsersDeal
from app.settings import DATABASE_SERVER, DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT, DATABASE_NAME

client = None
db = None

async def get_bank_accounts_list_by_username(username: str):
    bank_accounts = await db["UsersBankAccounts"].find({"username":username}).to_list(length=5)
    return list(bank_accounts)
# UsersBankAccounts
async def create_user_bank_account(bank_account: UsersBankAccount):
    try:
        res = await db["UsersBankAccounts"].insert_one(bank_account.__dict__)
        return True
    except:
        return False

async def delete_user_bank_account(username: str, account_number: str):
    res = await db["UsersBankAccounts"].delete_one({"username": username, "account_number": account_number})
    return res.deleted_count

async def get_users_account(username: str, account_number: str):
    users_account = await db["UsersBankAccounts"].find_one({"username": username, "account_number": account_number})
    return users_account
    
# BankAccounts   
async def get_account_monthly_balance(bank_account, year: int, month: int):
    account_monthly_balance = await db["BankAccounts"].find_one({"owner": bank_account["owner"], \
    "ssn": bank_account["ssn"], "account_number":bank_account["account_number"], "year": year, "month": month})
    return account_monthly_balance

async def get_account_monthly_balance_by_number(username: str, account_number: str, year: int, month: int):
    account_monthly_balance = await db["BankAccounts"].find_one({"username": username, "account_number": account_number, "year": year, "month": month})
    return account_monthly_balance
# UsersDeals
async def insert_users_deal(users_deal: UsersDeal):
    try:
        res = await db["UsersDeals"].insert_one(users_deal.__dict__)
        return True
    except:
        return False
