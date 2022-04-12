from urllib.parse import quote_plus
from pymongo import MongoClient
from uuid import uuid4
from app.models.bankaccountmodel import BankAccountByUsername, BankAccountBalance
from app.settings import DATABASE_SERVER, DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT, DATABASE_NAME

client = MongoClient(host=f'mongodb://{DATABASE_USER}:{quote_plus(DATABASE_PASSWORD)}@{DATABASE_SERVER}:{DATABASE_PORT}/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@tal-project-db@')
db = client[DATABASE_NAME]

#def insert_user(new_user, hashed_password):
    #user = UserInDB(**(new_user.__dict__))
    #user.hashed_password = hashed_password
    #user.id = uuid4()
    #ret = db.Users.insert_one(user.dict(by_alias=True))
    #return {'user': user}
def get_bank_accounts_list_by_username(username: str):
    bank_accounts_list = []
    bank_accounts_cur = list(db.UsersBankAccounts.find({"username":username}))
    for bank_account in bank_accounts_cur:
        del bank_account['_id']
        bank_accounts_list.append(BankAccountByUsername(**bank_account))
    return bank_accounts_list

def get_monthly_balance(bank_accounts_list, year, month):
    accounts_monthly_balance_list = []
    for bank_account in bank_accounts_list:
        account_monthly_balance = db.BankAccounts.find_one({"owner": bank_account.owner, \
        "ssn": bank_account.ssn, "account_number":bank_account.account_number, "year": year, "month": month})
        try:
            for transaction in account_monthly_balance['expenses_and_revenues']:
                accounts_monthly_balance_list.append(transaction)
        except Exception:
            pass
    return accounts_monthly_balance_list 




