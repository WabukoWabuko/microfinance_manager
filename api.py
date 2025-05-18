from fastapi import FastAPI, Depends
from handlers import login, create_user, create_group, create_contribution, create_loan, create_payout, sync_data, get_db
from entities import LoginRequest, UserCreate, GroupCreate, ContributionCreate, LoanCreate, PayoutCreate
from sqlalchemy.orm import Session

app = FastAPI()

@app.post("/login")
async def login_endpoint(request: LoginRequest, db: Session = Depends(get_db)):
    return await login(request, db)

@app.post("/users")
async def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return await create_user(user, db)

@app.post("/groups")
async def create_group_endpoint(group: GroupCreate, db: Session = Depends(get_db)):
    return await create_group(group, db)

@app.post("/contributions")
async def create_contribution_endpoint(contribution: ContributionCreate, db: Session = Depends(get_db)):
    return await create_contribution(contribution, db)

@app.post("/loans")
async def create_loan_endpoint(loan: LoanCreate, db: Session = Depends(get_db)):
    return await create_loan(loan, db)

@app.post("/payouts")
async def create_payout_endpoint(payout: PayoutCreate, db: Session = Depends(get_db)):
    return await create_payout(payout, db)

@app.post("/sync")
async def sync_endpoint(data: dict, db: Session = Depends(get_db)):
    return await sync_data(data, db)
