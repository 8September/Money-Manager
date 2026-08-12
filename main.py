from fastapi import FastAPI, HTTPException

app = FastAPI()


accounts = {}
transactions = {}

next_account_id = 1
next_transaction_id = 1


@app.post("/account/{account_id}/transactions")
async def create_transaction(account_id: int, data: dict):

    global next_transaction_id

    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")

    transaction = {
        "id": next_transaction_id,
        "account_id": account_id,
        "type": data.get("type", ""),  # income, expence
        "amount": data.get("amount", 0),
        "comment": data.get("comment", ""),
    }

    transactions[next_transaction_id] = transaction
    next_transaction_id += 1

    return transaction


@app.get("/accounts/{account_id}/balance")
async def get_balance(account_id: int):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")

    balance = 0

    for transaction in transactions.values():
        if transaction["account_id"] == account_id:
            if transaction["type"] == "income":
                balance += transaction["amount"]
            else:
                balance -= transaction["amount"]
    return {
        "account_id": account_id,
        "balance": balance,
    }


@app.post("/account")
async def create_account(data: dict):
    global next_account_id

    account = {
        "id": next_account_id,
        "name": data.get("name", ""),
    }

    accounts[next_account_id] = account
    next_account_id += 1

    return account


@app.put("/accounts/{account_id}")
async def update_account(account_id: int, data: dict):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")

    account = accounts[account_id]
    account["name"] = data.get("name", "")

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
