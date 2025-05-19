from fastapi import FastAPI, Depends
from handlers import (
    login, create_user, update_user, delete_user,
    create_group, update_group, delete_group,
    create_contribution, update_contribution, delete_contribution,
    create_loan, update_loan, delete_loan,
    create_payout, update_payout, delete_payout,
    sync_data, get_db
)
from entities import (
    LoginRequest, UserCreate, GroupCreate,
    ContributionCreate, LoanCreate, PayoutCreate, SyncEntry
)
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

@app.post("/login")
async def login_endpoint(request: LoginRequest, db: Session = Depends(get_db)):
    return await login(request, db)

@app.post("/users")
async def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return await create_user(user, db)

@app.put("/users/{user_id}")
async def update_user_endpoint(user_id: str, user: UserCreate, db: Session = Depends(get_db)):
    return await update_user(user_id, user, db)

@app.delete("/users/{user_id}")
async def delete_user_endpoint(user_id: str, db: Session = Depends(get_db)):
    return await delete_user(user_id, db)

@app.post("/groups")
async def create_group_endpoint(group: GroupCreate, db: Session = Depends(get_db)):
    return await create_group(group, db)

@app.put("/groups/{group_id}")
async def update_group_endpoint(group_id: str, group: GroupCreate, db: Session = Depends(get_db)):
    return await update_group(group_id, group, db)

@app.delete("/groups/{group_id}")
async def delete_group_endpoint(group_id: str, db: Session = Depends(get_db)):
    return await delete_group(group_id, db)

@app.post("/contributions")
async def create_contribution_endpoint(contribution: ContributionCreate, db: Session = Depends(get_db)):
    return await create_contribution(contribution, db)

@app.put("/contributions/{contribution_id}")
async def update_contribution_endpoint(contribution_id: str, contribution: ContributionCreate, db: Session = Depends(get_db)):
    return await update_contribution(contribution_id, contribution, db)

@app.delete("/contributions/{contribution_id}")
async def delete_contribution_endpoint(contribution_id: str, db: Session = Depends(get_db)):
    return await delete_contribution(contribution_id, db)

@app.post("/loans")
async def create_loan_endpoint(loan: LoanCreate, db: Session = Depends(get_db)):
    return await create_loan(loan, db)

@app.put("/loans/{loan_id}")
async def update_loan_endpoint(loan_id: str, loan: LoanCreate, db: Session = Depends(get_db)):
    return await update_loan(loan_id, loan, db)

@app.delete("/loans/{loan_id}")
async def delete_loan_endpoint(loan_id: str, db: Session = Depends(get_db)):
    return await delete_loan(loan_id, db)

@app.post("/payouts")
async def create_payout_endpoint(payout: PayoutCreate, db: Session = Depends(get_db)):
    return await create_payout(payout, db)

@app.put("/payouts/{payout_id}")
async def update_payout_endpoint(payout_id: str, payout: PayoutCreate, db: Session = Depends(get_db)):
    return await update_payout(payout_id, payout, db)

@app.delete("/payouts/{payout_id}")
async def delete_payout_endpoint(payout_id: str, db: Session = Depends(get_db)):
    return await delete_payout(payout_id, db)

@app.post("/sync")
async def sync_endpoint(entries: List[SyncEntry], db: Session = Depends(get_db)):
    return await sync_data(entries, db)
