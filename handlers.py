from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from entities import Base, User, Group, Contribution, Loan, Payout
from datetime import datetime
import json
import os
import jwt

class DatabaseHandler:
    def __init__(self):
        self.engine = create_engine(os.getenv('DATABASE_URL'))
        self.Session = sessionmaker(bind=self.engine)
        self.initialize_database()

    def initialize_database(self):
        with self.engine.connect() as conn:
            # Drop existing tables to ensure clean schema
            conn.execute(text("DROP TABLE IF EXISTS sync_queue CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS payouts CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS loans CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS contributions CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS groups CASCADE"))

            # Create tables with VARCHAR(36) for IDs
            conn.execute(text("""
                CREATE TABLE groups (
                    id VARCHAR(36) PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    balance FLOAT NOT NULL
                )
            """))
            conn.execute(text("""
                CREATE TABLE users (
                    id VARCHAR(36) PRIMARY KEY,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    group_id VARCHAR(36),
                    FOREIGN KEY (group_id) REFERENCES groups(id)
                )
            """))
            conn.execute(text("""
                CREATE TABLE contributions (
                    id VARCHAR(36) PRIMARY KEY,
                    user_id VARCHAR(36) NOT NULL,
                    group_id VARCHAR(36) NOT NULL,
                    amount FLOAT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (group_id) REFERENCES groups(id)
                )
            """))
            conn.execute(text("""
                CREATE TABLE loans (
                    id VARCHAR(36) PRIMARY KEY,
                    user_id VARCHAR(36) NOT NULL,
                    group_id VARCHAR(36) NOT NULL,
                    amount FLOAT NOT NULL,
                    interest_rate FLOAT NOT NULL,
                    due_date TIMESTAMP NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (group_id) REFERENCES groups(id)
                )
            """))
            conn.execute(text("""
                CREATE TABLE payouts (
                    id VARCHAR(36) PRIMARY KEY,
                    group_id VARCHAR(36) NOT NULL,
                    user_id VARCHAR(36) NOT NULL,
                    amount FLOAT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    FOREIGN KEY (group_id) REFERENCES groups(id),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """))
            conn.execute(text("""
                CREATE TABLE sync_queue (
                    id VARCHAR(36) PRIMARY KEY,
                    operation TEXT NOT NULL,
                    entity TEXT NOT NULL,
                    entity_id VARCHAR(36) NOT NULL,
                    data JSONB NOT NULL,
                    created_at TIMESTAMP NOT NULL
                )
            """))

            # Create indexes for performance
            conn.execute(text("CREATE INDEX idx_users_username ON users(username)"))
            conn.execute(text("CREATE INDEX idx_groups_name ON groups(name)"))
            conn.execute(text("CREATE INDEX idx_contributions_user_id ON contributions(user_id)"))
            conn.execute(text("CREATE INDEX idx_contributions_group_id ON contributions(group_id)"))
            conn.execute(text("CREATE INDEX idx_loans_user_id ON loans(user_id)"))
            conn.execute(text("CREATE INDEX idx_loans_group_id ON loans(group_id)"))
            conn.execute(text("CREATE INDEX idx_payouts_group_id ON payouts(group_id)"))
            conn.execute(text("CREATE INDEX idx_payouts_user_id ON payouts(user_id)"))
            conn.execute(text("CREATE INDEX idx_sync_queue_entity ON sync_queue(entity)"))

            conn.commit()

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
            return session.query(User).filter_by(id=user_id).first()
        finally:
            session.close()

    def get_user_by_username(self, username):
        session = self.Session()
        try:
            return session.query(User).filter_by(username=username).first()
        finally:
            session.close()

    def get_all_users(self):
        session = self.Session()
        try:
            return session.query(User).all()
        finally:
            session.close()

    def update_user(self, user_id, username=None, password=None, role=None, group_id=None):
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                if username:
                    user.username = username
                if password and password != "unchanged":
                    user.password = password
                if role:
                    user.role = role
                if group_id:
                    user.group_id = group_id
                session.commit()
            return user
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_user(self, user_id):
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                session.delete(user)
                session.commit()
        except:
            session.rollback()
            raise
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
            return session.query(Group).filter_by(id=group_id).first()
        finally:
            session.close()

    def get_all_groups(self):
        session = self.Session()
        try:
            return session.query(Group).all()
        finally:
            session.close()

    def update_group(self, group_id, name=None, description=None, balance=None):
        session = self.Session()
        try:
            group = session.query(Group).filter_by(id=group_id).first()
            if group:
                if name:
                    group.name = name
                if description is not None:
                    group.description = description
                if balance is not None:
                    group.balance = balance
                session.commit()
            return group
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_group(self, group_id):
        session = self.Session()
        try:
            group = session.query(Group).filter_by(id=group_id).first()
            if group:
                session.delete(group)
                session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def create_contribution(self, user_id, group_id, amount):
        session = self.Session()
        try:
            contribution = Contribution(user_id=user_id, group_id=group_id, amount=amount)
            group = session.query(Group).filter_by(id=group_id).first()
            if group:
                group.balance += amount
            session.add(contribution)
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
            return session.query(Contribution).filter_by(id=contribution_id).first()
        finally:
            session.close()

    def get_all_contributions(self):
        session = self.Session()
        try:
            return session.query(Contribution).all()
        finally:
            session.close()

    def update_contribution(self, contribution_id, user_id=None, group_id=None, amount=None):
        session = self.Session()
        try:
            contribution = session.query(Contribution).filter_by(id=contribution_id).first()
            if contribution:
                old_amount = contribution.amount
                old_group_id = contribution.group_id
                if user_id:
                    contribution.user_id = user_id
                if group_id:
                    contribution.group_id = group_id
                if amount is not None:
                    contribution.amount = amount
                if amount is not None or group_id:
                    old_group = session.query(Group).filter_by(id=old_group_id).first()
                    if old_group:
                        old_group.balance -= old_amount
                    new_group = session.query(Group).filter_by(id=contribution.group_id).first()
                    if new_group:
                        new_group.balance += contribution.amount
                session.commit()
            return contribution
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_contribution(self, contribution_id):
        session = self.Session()
        try:
            contribution = session.query(Contribution).filter_by(id=contribution_id).first()
            if contribution:
                group = session.query(Group).filter_by(id=contribution.group_id).first()
                if group:
                    group.balance -= contribution.amount
                session.delete(contribution)
                session.commit()
        except:
            session.rollback()
            raise
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
            group = session.query(Group).filter_by(id=group_id).first()
            if group:
                group.balance -= amount
            session.add(loan)
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
            return session.query(Loan).filter_by(id=loan_id).first()
        finally:
            session.close()

    def get_all_loans(self):
        session = self.Session()
        try:
            return session.query(Loan).all()
        finally:
            session.close()

    def update_loan(self, loan_id, user_id=None, group_id=None, amount=None, interest_rate=None, due_date=None):
        session = self.Session()
        try:
            loan = session.query(Loan).filter_by(id=loan_id).first()
            if loan:
                old_amount = loan.amount
                old_group_id = loan.group_id
                if user_id:
                    loan.user_id = user_id
                if group_id:
                    loan.group_id = group_id
                if amount is not None:
                    loan.amount = amount
                if interest_rate is not None:
                    loan.interest_rate = interest_rate
                if due_date:
                    loan.due_date = datetime.fromisoformat(due_date)
                if amount is not None or group_id:
                    old_group = session.query(Group).filter_by(id=old_group_id).first()
                    if old_group:
                        old_group.balance += old_amount
                    new_group = session.query(Group).filter_by(id=loan.group_id).first()
                    if new_group:
                        new_group.balance -= loan.amount
                session.commit()
            return loan
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_loan(self, loan_id):
        session = self.Session()
        try:
            loan = session.query(Loan).filter_by(id=loan_id).first()
            if loan:
                group = session.query(Group).filter_by(id=loan.group_id).first()
                if group:
                    group.balance += loan.amount
                session.delete(loan)
                session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def create_payout(self, group_id, user_id, amount):
        session = self.Session()
        try:
            payout = Payout(group_id=group_id, user_id=user_id, amount=amount)
            group = session.query(Group).filter_by(id=group_id).first()
            if group:
                group.balance -= amount
            session.add(payout)
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
            return session.query(Payout).filter_by(id=payout_id).first()
        finally:
            session.close()

    def get_all_payouts(self):
        session = self.Session()
        try:
            return session.query(Payout).all()
        finally:
            session.close()

    def update_payout(self, payout_id, group_id=None, user_id=None, amount=None):
        session = self.Session()
        try:
            payout = session.query(Payout).filter_by(id=payout_id).first()
            if payout:
                old_amount = payout.amount
                old_group_id = payout.group_id
                if group_id:
                    payout.group_id = group_id
                if user_id:
                    payout.user_id = user_id
                if amount is not None:
                    payout.amount = amount
                if amount is not None or group_id:
                    old_group = session.query(Group).filter_by(id=old_group_id).first()
                    if old_group:
                        old_group.balance += old_amount
                    new_group = session.query(Group).filter_by(id=payout.group_id).first()
                    if new_group:
                        new_group.balance -= payout.amount
                session.commit()
            return payout
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_payout(self, payout_id):
        session = self.Session()
        try:
            payout = session.query(Payout).filter_by(id=payout_id).first()
            if payout:
                group = session.query(Group).filter_by(id=payout.group_id).first()
                if group:
                    group.balance += payout.amount
                session.delete(payout)
                session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def authenticate(self, username, password):
        session = self.Session()
        try:
            user = session.query(User).filter_by(username=username, password=password).first()
            if user:
                token = jwt.encode(
                    {'user_id': user.id, 'username': user.username, 'role': user.role},
                    'secret_key',
                    algorithm='HS256'
                )
                return token
            return None
        finally:
            session.close()

    def process_sync(self, entries):
        session = self.Session()
        results = []
        try:
            for entry in entries:
                result = {'id': entry['id'], 'status': 'success'}
                try:
                    entity = entry['entity']
                    operation = entry['operation']
                    entity_id = entry['entity_id']
                    data = entry['data']

                    if entity == 'user':
                        if operation == 'insert':
                            user = User(id=entity_id, **data)
                            session.add(user)
                        elif operation == 'update':
                            user = session.query(User).filter_by(id=entity_id).first()
                            if user:
                                for key, value in data.items():
                                    setattr(user, key, value)
                        elif operation == 'delete':
                            user = session.query(User).filter_by(id=entity_id).first()
                            if user:
                                session.delete(user)
                    elif entity == 'group':
                        if operation == 'insert':
                            group = Group(id=entity_id, **data)
                            session.add(group)
                        elif operation == 'update':
                            group = session.query(Group).filter_by(id=entity_id).first()
                            if group:
                                for key, value in data.items():
                                    setattr(group, key, value)
                        elif operation == 'delete':
                            group = session.query(Group).filter_by(id=entity_id).first()
                            if group:
                                session.delete(group)
                    elif entity == 'contribution':
                        if operation == 'insert':
                            contribution = Contribution(id=entity_id, **data)
                            session.add(contribution)
                            group = session.query(Group).filter_by(id=data['group_id']).first()
                            if group:
                                group.balance += data['amount']
                        elif operation == 'update':
                            contribution = session.query(Contribution).filter_by(id=entity_id).first()
                            if contribution:
                                old_amount = contribution.amount
                                old_group_id = contribution.group_id
                                for key, value in data.items():
                                    setattr(contribution, key, value)
                                old_group = session.query(Group).filter_by(id=old_group_id).first()
                                if old_group:
                                    old_group.balance -= old_amount
                                new_group = session.query(Group).filter_by(id=data['group_id']).first()
                                if new_group:
                                    new_group.balance += data['amount']
                        elif operation == 'delete':
                            contribution = session.query(Contribution).filter_by(id=entity_id).first()
                            if contribution:
                                group = session.query(Group).filter_by(id=contribution.group_id).first()
                                if group:
                                    group.balance -= contribution.amount
                                session.delete(contribution)
                    elif entity == 'loan':
                        if operation == 'insert':
                            data['due_date'] = datetime.fromisoformat(data['due_date'])
                            loan = Loan(id=entity_id, **data)
                            session.add(loan)
                            group = session.query(Group).filter_by(id=data['group_id']).first()
                            if group:
                                group.balance -= data['amount']
                        elif operation == 'update':
                            loan = session.query(Loan).filter_by(id=entity_id).first()
                            if loan:
                                old_amount = loan.amount
                                old_group_id = loan.group_id
                                for key, value in data.items():
                                    if key == 'due_date':
                                        value = datetime.fromisoformat(value)
                                    setattr(loan, key, value)
                                old_group = session.query(Group).filter_by(id=old_group_id).first()
                                if old_group:
                                    old_group.balance += old_amount
                                new_group = session.query(Group).filter_by(id=data['group_id']).first()
                                if new_group:
                                    new_group.balance -= data['amount']
                        elif operation == 'delete':
                            loan = session.query(Loan).filter_by(id=entity_id).first()
                            if loan:
                                group = session.query(Group).filter_by(id=loan.group_id).first()
                                if group:
                                    group.balance += loan.amount
                                session.delete(loan)
                    elif entity == 'payout':
                        if operation == 'insert':
                            payout = Payout(id=entity_id, **data)
                            session.add(payout)
                            group = session.query(Group).filter_by(id=data['group_id']).first()
                            if group:
                                group.balance -= data['amount']
                        elif operation == 'update':
                            payout = session.query(Payout).filter_by(id=entity_id).first()
                            if payout:
                                old_amount = payout.amount
                                old_group_id = payout.group_id
                                for key, value in data.items():
                                    setattr(payout, key, value)
                                old_group = session.query(Group).filter_by(id=old_group_id).first()
                                if old_group:
                                    old_group.balance += old_amount
                                new_group = session.query(Group).filter_by(id=data['group_id']).first()
                                if new_group:
                                    new_group.balance -= data['amount']
                        elif operation == 'delete':
                            payout = session.query(Payout).filter_by(id=entity_id).first()
                            if payout:
                                group = session.query(Group).filter_by(id=payout.group_id).first()
                                if group:
                                    group.balance += payout.amount
                                session.delete(payout)
                except Exception as e:
                    result['status'] = 'error'
                    result['error'] = str(e)
                results.append(result)
            session.commit()
            return results
        except:
            session.rollback()
            raise
        finally:
            session.close()
