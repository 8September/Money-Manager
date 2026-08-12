from fastapi import FastAPI, HTTPException

from pydantic import BaseModel, Field

from enum import Enum

from decimal import Decimal

app = FastAPI()

accounts = {}
transactions = {}

next_account_id = 1
next_transaction_id = 1


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class TransactionCreate(BaseModel):
    transaction_type: TransactionType
    amount: Decimal = Field(..., gt=0, max_digits=12, decimal_places=2)
    comment: str = Field("", max_length=120)


class TransactionRead(BaseModel):
    id: int
    account_id: int
    transaction_type: TransactionType
    amount: Decimal
    comment: str


class AccountCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=20)


class AccountRead(BaseModel):
    name: str


class BalanceRead(BaseModel):
    account_id: int
    balance: Decimal


async def calculate_balance(account_id: int) -> Decimal:
    balance = Decimal("0")

    for transaction in transactions.values():
        if transaction["account_id"] == account_id:
            if transaction["type"] == TransactionType.INCOME:
                balance += transaction["amount"]
            else:
                balance -= transaction["amount"]
    return balance


@app.post("/account/{account_id}/transactions", response_model=TransactionRead)
async def create_transaction(account_id: int, data: TransactionCreate):

    global next_transaction_id

    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")

    transaction = {
        "id": next_transaction_id,
        "account_id": account_id,
        "type": data.transaction_type,  # income, expence
        "amount": data.amount,
        "comment": data.comment,
    }

    transactions[next_transaction_id] = transaction
    next_transaction_id += 1

    return transaction


@app.get("/accounts/{account_id}/balance", response_model=BalanceRead)
async def get_balance(account_id: int):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")

    return {
        "account_id": account_id,
        "balance": await calculate_balance(account_id),
    }


@app.post("/account")
async def create_account(data: AccountCreate):
    global next_account_id

    account = {
        "id": next_account_id,
        "name": data.name,
    }

    accounts[next_account_id] = account
    next_account_id += 1

    return account


@app.put("/accounts/{account_id}")
async def update_account(account_id: int, data: AccountRead):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")

    account = accounts[account_id]
    account["name"] = data.name

    return account


@app.delete("/accounts/{account_id}")
async def delete_account(account_id: int):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")

    del accounts[account_id]

    return {"message": "Account was deleted"}


@app.get("/accounts")
async def get_account():
    return list(accounts.values())


@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}


@app.get("/about")
async def read_about():
    return {"Project": "Money Manager"}
