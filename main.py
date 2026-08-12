from fastapi import FastAPI, HTTPException

app = FastAPI()


accounts = {}
transactions = {}

next_account_id = 1
next_transaction_id = 1


@app.post("/balance")
async def create_balance(data: dict):
    global next_transaction_id

    balance = {"id": next_transaction_id, "balance": data.get("balance", "")}

    transactions[next_transaction_id] = balance
    next_transaction_id += 1


@app.post('/account')
async def create_account(data: dict):
    global next_account_id

    account = {'id': next_account_id, 'name': data.get('name', '')}

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


@app.get('/accounts')
async def get_account():
    return list(accounts.values())


@app.get('/')
async def read_root():
    return {'message': 'Hello, world!'}


@app.get('/about')
async def read_about():
    return {'Project': 'Money Manager'}
