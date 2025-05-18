from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from pydantic import BaseModel, constr
import uuid

Base = declarative_base()

# SQLAlchemy models for SQLite (local) and PostgreSQL (cloud)
class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Hashed with bcrypt
    role = Column(String, nullable=False)
    group_id = Column(UUID(as_uuid=True), ForeignKey('groups.id'), nullable=True)

class Group(Base):
    __tablename__ = 'groups'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    balance = Column(Float, nullable=False, default=0.0)

class Contribution(Base):
    __tablename__ = 'contributions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    group_id = Column(UUID(as_uuid=True), ForeignKey('groups.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String, nullable=False, default='pending')

class Loan(Base):
    __tablename__ = 'loans'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    group_id = Column(UUID(as_uuid=True), ForeignKey('groups.id'), nullable=False)
    amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    date_issued = Column(DateTime, nullable=False, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, default='active')

class Payout(Base):
    __tablename__ = 'payouts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_id = Column(UUID(as_uuid=True), ForeignKey('groups.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String, nullable=False, default='pending')

class SyncQueue(Base):
    __tablename__ = 'sync_queue'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    operation = Column(String, nullable=False)
    entity = Column(String, nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=False)
    data = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

# Pydantic models for API validation
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
