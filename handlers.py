from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from entities import User, Group, Contribution, Loan, Payout, UserCreate, LoginRequest, GroupCreate, ContributionCreate, LoanCreate, PayoutCreate, SyncEntry
import bcrypt
from auth import create_jwt
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from datetime import datetime

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
        id=str(uuid.uuid4()),
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

async def update_user(user_id: str, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user.username
    db_user.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db_user.role = user.role
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")

async def delete_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted"}

async def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    db_group = Group(
        id=str(uuid.uuid4()),
        name=group.name,
        description=group.description,
        balance=group.balance
    )
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

async def update_group(group_id: str, group: GroupCreate, db: Session = Depends(get_db)):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    db_group.name = group.name
    db_group.description = group.description
    db_group.balance = group.balance
    db.commit()
    db.refresh(db_group)
    return db_group

async def delete_group(group_id: str, db: Session = Depends(get_db)):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    db.delete(db_group)
    db.commit()
    return {"detail": "Group deleted"}

async def create_contribution(contribution: ContributionCreate, db: Session = Depends(get_db)):
    db_contribution = Contribution(
        id=str(uuid.uuid4()),
        user_id=contribution.user_id,
        group_id=contribution.group_id,
        amount=contribution.amount
    )
    db.add(db_contribution)
    db.commit()
    db.refresh(db_contribution)
    return db_contribution

async def update_contribution(contribution_id: str, contribution: ContributionCreate, db: Session = Depends(get_db)):
    db_contribution = db.query(Contribution).filter(Contribution.id == contribution_id).first()
    if not db_contribution:
        raise HTTPException(status_code=404, detail="Contribution not found")
    db_contribution.user_id = contribution.user_id
    db_contribution.group_id = contribution.group_id
    db_contribution.amount = contribution.amount
    db.commit()
    db.refresh(db_contribution)
    return db_contribution

async def delete_contribution(contribution_id: str, db: Session = Depends(get_db)):
    db_contribution = db.query(Contribution).filter(Contribution.id == contribution_id).first()
    if not db_contribution:
        raise HTTPException(status_code=404, detail="Contribution not found")
    db.delete(db_contribution)
    db.commit()
    return {"detail": "Contribution deleted"}

async def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    db_loan = Loan(
        id=str(uuid.uuid4()),
        user_id=loan.user_id,
        group_id=loan.group_id,
        amount=loan.amount,
        interest_rate=loan.interest_rate,
        due_date=datetime.fromisoformat(loan.due_date)
    )
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

async def update_loan(loan_id: str, loan: LoanCreate, db: Session = Depends(get_db)):
    db_loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    db_loan.user_id = loan.user_id
    db_loan.group_id = loan.group_id
    db_loan.amount = loan.amount
    db_loan.interest_rate = loan.interest_rate
    db_loan.due_date = datetime.fromisoformat(loan.due_date)
    db.commit()
    db.refresh(db_loan)
    return db_loan

async def delete_loan(loan_id: str, db: Session = Depends(get_db)):
    db_loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not db_loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    db.delete(db_loan)
    db.commit()
    return {"detail": "Loan deleted"}

async def create_payout(payout: PayoutCreate, db: Session = Depends(get_db)):
    db_payout = Payout(
        id=str(uuid.uuid4()),
        group_id=payout.group_id,
        user_id=payout.user_id,
        amount=payout.amount
    )
    db.add(db_payout)
    db.commit()
    db.refresh(db_payout)
    return db_payout

async def update_payout(payout_id: str, payout: PayoutCreate, db: Session = Depends(get_db)):
    db_payout = db.query(Payout).filter(Payout.id == payout_id).first()
    if not db_payout:
        raise HTTPException(status_code=404, detail="Payout not found")
    db_payout.group_id = payout.group_id
    db_payout.user_id = payout.user_id
    db_payout.amount = payout.amount
    db.commit()
    db.refresh(db_payout)
    return db_payout

async def delete_payout(payout_id: str, db: Session = Depends(get_db)):
    db_payout = db.query(Payout).filter(Payout.id == payout_id).first()
    if not db_payout:
        raise HTTPException(status_code=404, detail="Payout not found")
    db.delete(db_payout)
    db.commit()
    return {"detail": "Payout deleted"}

async def sync_data(entries: list[SyncEntry], db: Session = Depends(get_db)):
    results = []
    for entry in entries:
        try:
            if entry.operation == "insert":
                if entry.entity == "user":
                    db_user = User(
                        id=entry.entity_id,
                        username=entry.data["username"],
                        password=entry.data.get("password", ""),
                        role=entry.data["role"]
                    )
                    db.add(db_user)
                elif entry.entity == "group":
                    db_group = Group(
                        id=entry.entity_id,
                        name=entry.data["name"],
                        description=entry.data.get("description"),
                        balance=entry.data.get("balance", 0.0)
                    )
                    db.add(db_group)
                elif entry.entity == "contribution":
                    db_contribution = Contribution(
                        id=entry.entity_id,
                        user_id=entry.data["user_id"],
                        group_id=entry.data["group_id"],
                        amount=entry.data["amount"]
                    )
                    db.add(db_contribution)
                elif entry.entity == "loan":
                    db_loan = Loan(
                        id=entry.entity_id,
                        user_id=entry.data["user_id"],
                        group_id=entry.data["group_id"],
                        amount=entry.data["amount"],
                        interest_rate=entry.data.get("interest_rate", 5.0),
                        due_date=datetime.fromisoformat(entry.data["due_date"])
                    )
                    db.add(db_loan)
                elif entry.entity == "payout":
                    db_payout = Payout(
                        id=entry.entity_id,
                        group_id=entry.data["group_id"],
                        user_id=entry.data["user_id"],
                        amount=entry.data["amount"]
                    )
                    db.add(db_payout)
                else:
                    results.append({"id": entry.id, "status": "failed", "error": "Unknown entity"})
                    continue
                db.commit()
                results.append({"id": entry.id, "status": "success"})
            elif entry.operation == "update":
                if entry.entity == "user":
                    db_user = db.query(User).filter(User.id == entry.entity_id).first()
                    if db_user:
                        db_user.username = entry.data["username"]
                        db_user.role = entry.data["role"]
                        db_user.group_id = entry.data.get("group_id")
                        db.commit()
                elif entry.entity == "group":
                    db_group = db.query(Group).filter(Group.id == entry.entity_id).first()
                    if db_group:
                        db_group.name = entry.data["name"]
                        db_group.description = entry.data.get("description")
                        db_group.balance = entry.data["balance"]
                        db.commit()
                elif entry.entity == "contribution":
                    db_contribution = db.query(Contribution).filter(Contribution.id == entry.entity_id).first()
                    if db_contribution:
                        db_contribution.user_id = entry.data["user_id"]
                        db_contribution.group_id = entry.data["group_id"]
                        db_contribution.amount = entry.data["amount"]
                        db.commit()
                elif entry.entity == "loan":
                    db_loan = db.query(Loan).filter(Loan.id == entry.entity_id).first()
                    if db_loan:
                        db_loan.user_id = entry.data["user_id"]
                        db_loan.group_id = entry.data["group_id"]
                        db_loan.amount = entry.data["amount"]
                        db_loan.interest_rate = entry.data["interest_rate"]
                        db_loan.due_date = datetime.fromisoformat(entry.data["due_date"])
                        db.commit()
                elif entry.entity == "payout":
                    db_payout = db.query(Payout).filter(Payout.id == entry.entity_id).first()
                    if db_payout:
                        db_payout.group_id = entry.data["group_id"]
                        db_payout.user_id = entry.data["user_id"]
                        db_payout.amount = entry.data["amount"]
                        db.commit()
                else:
                    results.append({"id": entry.id, "status": "failed", "error": "Unknown entity"})
                    continue
                results.append({"id": entry.id, "status": "success"})
            elif entry.operation == "delete":
                if entry.entity == "user":
                    db_user = db.query(User).filter(User.id == entry.entity_id).first()
                    if db_user:
                        db.delete(db_user)
                        db.commit()
                elif entry.entity == "group":
                    db_group = db.query(Group).filter(Group.id == entry.entity_id).first()
                    if db_group:
                        db.delete(db_group)
                        db.commit()
                elif entry.entity == "contribution":
                    db_contribution = db.query(Contribution).filter(Contribution.id == entry.entity_id).first()
                    if db_contribution:
                        db.delete(db_contribution)
                        db.commit()
                elif entry.entity == "loan":
                    db_loan = db.query(Loan).filter(Loan.id == entry.entity_id).first()
                    if db_loan:
                        db.delete(db_loan)
                        db.commit()
                elif entry.entity == "payout":
                    db_payout = db.query(Payout).filter(Payout.id == entry.entity_id).first()
                    if db_payout:
                        db.delete(db_payout)
                        db.commit()
                else:
                    results.append({"id": entry.id, "status": "failed", "error": "Unknown entity"})
                    continue
                results.append({"id": entry.id, "status": "success"})
            else:
                results.append({"id": entry.id, "status": "failed", "error": "Operation not supported"})
        except Exception as e:
            db.rollback()
            results.append({"id": entry.id, "status": "failed", "error": str(e)})
    return {"results": results}
