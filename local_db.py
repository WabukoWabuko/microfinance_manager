from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entities import Base, User, Group, Contribution, Loan, Payout, SyncQueue
import json
from datetime import datetime

class LocalDatabase:
    def __init__(self):
        self.engine = create_engine('sqlite:///microfinance.db')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_user(self, username, password, role, group_id=None):
        session = self.Session()
        try:
            user = User(username=username, password=password, role=role, group_id=group_id)
            session.add(user)
            session.commit()
            return user.id
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def get_user(self, user_id):
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            return user
        finally:
            session.close()

    def get_user_by_username(self, username):
        session = self.Session()
        try:
            user = session.query(User).filter_by(username=username).first()
            return user
        finally:
            session.close()

    def create_group(self, name, description=None, balance=0.0):
        session = self.Session()
        try:
            group = Group(name=name, description=description, balance=balance)
            session.add(group)
            session.commit()
            return group.id
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def get_group(self, group_id):
        session = self.Session()
        try:
            group = session.query(Group).filter_by(id=group_id).first()
            return group
        finally:
            session.close()

    def create_contribution(self, user_id, group_id, amount):
        session = self.Session()
        try:
            contribution = Contribution(user_id=user_id, group_id=group_id, amount=amount)
            session.add(contribution)
            session.flush()  # Get contribution.id
            sync_entry = SyncQueue(
                operation='insert',
                entity='contribution',
                entity_id=contribution.id,
                data=json.dumps({'user_id': user_id, 'group_id': group_id, 'amount': amount})
            )
            session.add(sync_entry)
            session.commit()
            return contribution.id
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def get_contribution(self, contribution_id):
        session = self.Session()
        try:
            contribution = session.query(Contribution).filter_by(id=contribution_id).first()
            return contribution
        finally:
            session.close()

    def create_loan(self, user_id, group_id, amount, interest_rate, due_date):
        session = self.Session()
        try:
            loan = Loan(
                user_id=user_id,
                group_id=group_id,
                amount=amount,
                interest_rate=interest_rate,
                due_date=datetime.fromisoformat(due_date)
            )
            session.add(loan)
            session.flush()
            sync_entry = SyncQueue(
                operation='insert',
                entity='loan',
                entity_id=loan.id,
                data=json.dumps({'user_id': user_id, 'group_id': group_id, 'amount': amount})
            )
            session.add(sync_entry)
            session.commit()
            return loan.id
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def get_loan(self, loan_id):
        session = self.Session()
        try:
            loan = session.query(Loan).filter_by(id=loan_id).first()
            return loan
        finally:
            session.close()

    def create_payout(self, group_id, user_id, amount):
        session = self.Session()
        try:
            payout = Payout(group_id=group_id, user_id=user_id, amount=amount)
            session.add(payout)
            session.flush()
            sync_entry = SyncQueue(
                operation='insert',
                entity='payout',
                entity_id=payout.id,
                data=json.dumps({'group_id': group_id, 'user_id': user_id, 'amount': amount})
            )
            session.add(sync_entry)
            session.commit()
            return payout.id
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def get_payout(self, payout_id):
        session = self.Session()
        try:
            payout = session.query(Payout).filter_by(id=payout_id).first()
            return payout
        finally:
            session.close()

    def get_sync_queue(self, sync_id):
        session = self.Session()
        try:
            sync_entry = session.query(SyncQueue).filter_by(id=sync_id).first()
            return sync_entry
        finally:
            session.close()
