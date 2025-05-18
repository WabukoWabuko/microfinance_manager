from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from entities import User, Group, Contribution, Loan, Payout, UserCreate, LoginRequest, GroupCreate, ContributionCreate, LoanCreate, PayoutCreate
import bcrypt
from auth import create_jwt
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

def get_db():
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL.startswith("postgresql://"):
        raise ValueError("DATABASE_URL must start with 'postgresql://'")
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not bcrypt.checkpw(request.password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt(user.username)
    return {"token": token}

async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db_user = User(
        id=uuid.uuid4(),
        username=user.username,
        password=hashed_password,
        role=user.role
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")

async def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    db_group = Group(
        id=uuid.uuid4(),
        name=group.name,
        description=group.description,
        balance=group.balance
    )
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

async def create_contribution(contribution: ContributionCreate, db: Session = Depends(get_db)):
    db_contribution = Contribution(
        id=uuid.uuid4(),
        user_id=uuid.UUID(contribution.user_id),
        group_id=uuid.UUID(contribution.group_id),
        amount=contribution.amount
    )
    db.add(db_contribution)
    db.commit()
    db.refresh(db_contribution)
    return db_contribution

async def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    db_loan = Loan(
        id=uuid.uuid4(),
        user_id=uuid.UUID(loan.user_id),
        group_id=uuid.UUID(loan.group_id),
        amount=loan.amount,
        interest_rate=loan.interest_rate,
        due_date=datetime.fromisoformat(loan.due_date)
    )
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

async def create_payout(payout: PayoutCreate, db: Session = Depends(get_db)):
    db_payout = Payout(
        id=uuid.uuid4(),
        group_id=uuid.UUID(payout.group_id),
        user_id=uuid.UUID(payout.user_id),
        amount=payout.amount
    )
    db.add(db_payout)
    db.commit()
    db.refresh(db_payout)
    return db_payout

async def sync_data(data: dict, db: Session = Depends(get_db)):
    # Placeholder for sync logic
    return {"status": "Sync not implemented yet"}
