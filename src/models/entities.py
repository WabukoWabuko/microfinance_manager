from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Hashed in production
    role = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=True)

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    balance = Column(Float, nullable=False, default=0.0)

class Contribution(Base):
    __tablename__ = 'contributions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String, nullable=False, default='pending')

class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    date_issued = Column(DateTime, nullable=False, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, default='active')

class Payout(Base):
    __tablename__ = 'payouts'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String, nullable=False, default='pending')

class SyncQueue(Base):
    __tablename__ = 'sync_queue'
    id = Column(Integer, primary_key=True)
    operation = Column(String, nullable=False)
    entity = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=False)
    data = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
