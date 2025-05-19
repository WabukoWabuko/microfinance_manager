from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from pydantic import BaseModel, constr
import uuid

Base = declarative_base()

def uuid_str():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = 'users'
    id = Column(String(36), primary_key=True, default=uuid_str)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    group_id = Column(String(36), ForeignKey('groups.id'), nullable=True)

class Group(Base):
    __tablename__ = 'groups'
    id = Column(String(36), primary_key=True, default=uuid_str)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    balance = Column(Float, nullable=False, default=0.0)

class Contribution(Base):
    __tablename__ = 'contributions'
    id = Column(String(36), primary_key=True, default=uuid_str)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    group_id = Column(String(36), ForeignKey('groups.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String, nullable=False, default='pending')

class Loan(Base):
    __tablename__ = 'loans'
    id = Column(String(36), primary_key=True, default=uuid_str)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    group_id = Column(String(36), ForeignKey('groups.id'), nullable=False)
    amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    date_issued = Column(DateTime, nullable=False, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, default='active')

class Payout(Base):
    __tablename__ = 'payouts'
    id = Column(String(36), primary_key=True, default=uuid_str)
    group_id = Column(String(36), ForeignKey('groups.id'), nullable=False)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String, nullable=False, default='pending')

class SyncQueue(Base):
    __tablename__ = 'sync_queue'
    id = Column(String(36), primary_key=True, default=uuid_str)
    operation = Column(String, nullable=False)
    entity = Column(String, nullable=False)
    entity_id = Column(String(36), nullable=False)
    data = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=6)
    role: str

class LoginRequest(BaseModel):
    username: str
    password: str

class GroupCreate(BaseModel):
    name: str
    description: str | None = None
    balance: float = 0.0

class ContributionCreate(BaseModel):
    user_id: str
    group_id: str
    amount: float

class LoanCreate(BaseModel):
    user_id: str
    group_id: str
    amount: float
    interest_rate: float
    due_date: str

class PayoutCreate(BaseModel):
    group_id: str
    user_id: str
    amount: float

class SyncEntry(BaseModel):
    id: str
    operation: str
    entity: str
    entity_id: str
    data: dict
    created_at: str
