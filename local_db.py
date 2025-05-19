from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entities import Base, User, Group, Contribution, Loan, Payout, SyncQueue
import json
from datetime import datetime
import uuid
import sqlite3

class LocalDatabase:
    def __init__(self):
        self.engine = create_engine('sqlite:///microfinance.db')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.migrate_schema()

    def migrate_schema(self):
        conn = sqlite3.connect('microfinance.db')
        cursor = conn.cursor()
        session = self.Session()
        try:
            # Dictionary of tables and their models
            tables = {
                'users': User,
                'groups': Group,
                'contributions': Contribution,
                'loans': Loan,
                'payouts': Payout,
                'sync_queue': SyncQueue
            }

            for table_name, model in tables.items():
                # Check if table exists
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
                if not cursor.fetchone():
                    continue

                # Create temporary table with correct schema
                temp_table = f"{table_name}_temp"
                cursor.execute(f"DROP TABLE IF EXISTS {temp_table}")
                Base.metadata.tables[table_name].create(bind=self.engine, checkfirst=True)

                # Get columns from original table
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in cursor.fetchall()]
                columns_str = ', '.join(columns)

                # Copy data, converting IDs to UUID strings
                cursor.execute(f"INSERT INTO {temp_table} ({columns_str}) SELECT * FROM {table_name}")
                items = session.query(model).all()
                for item in items:
                    if not isinstance(item.id, str):
                        new_id = str(uuid.uuid4())
                        cursor.execute(f"UPDATE {temp_table} SET id = ? WHERE id = ?", (new_id, item.id))
                        item.id = new_id
                    if table_name in ['contributions', 'loans']:
                        if not isinstance(item.user_id, str):
                            new_user_id = str(uuid.uuid4())
                            cursor.execute(f"UPDATE {temp_table} SET user_id = ? WHERE user_id = ?", (new_user_id, item.user_id))
                            item.user_id = new_user_id
                        if not isinstance(item.group_id, str):
                            new_group_id = str(uuid.uuid4())
                            cursor.execute(f"UPDATE {temp_table} SET group_id = ? WHERE group_id = ?", (new_group_id, item.group_id))
                            item.group_id = new_group_id
                    elif table_name == 'payouts':
                        if not isinstance(item.group_id, str):
                            new_group_id = str(uuid.uuid4())
                            cursor.execute(f"UPDATE {temp_table} SET group_id = ? WHERE group_id = ?", (new_group_id, item.group_id))
                            item.group_id = new_group_id
                        if not isinstance(item.user_id, str):
                            new_user_id = str(uuid.uuid4())
                            cursor.execute(f"UPDATE {temp_table} SET user_id = ? WHERE user_id = ?", (new_user_id, item.user_id))
                            item.user_id = new_user_id
                    elif table_name == 'users' and item.group_id and not isinstance(item.group_id, str):
                        new_group_id = str(uuid.uuid4())
                        cursor.execute(f"UPDATE {temp_table} SET group_id = ? WHERE group_id = ?", (new_group_id, item.group_id))
                        item.group_id = new_group_id
                    elif table_name == 'sync_queue' and not isinstance(item.entity_id, str):
                        new_entity_id = str(uuid.uuid4())
                        cursor.execute(f"UPDATE {temp_table} SET entity_id = ? WHERE entity_id = ?", (new_entity_id, item.entity_id))
                        item.entity_id = new_entity_id
                session.commit()

                # Replace original table
                cursor.execute(f"DROP TABLE {table_name}")
                cursor.execute(f"ALTER TABLE {temp_table} RENAME TO {table_name}")

            conn.commit()
        except:
            conn.rollback()
            session.rollback()
            raise
        finally:
            session.close()
            conn.close()

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
                if password:
                    user.password = password
                if role:
                    user.role = role
                if group_id:
                    user.group_id = group_id
                session.commit()
                sync_entry = SyncQueue(
                    operation='update',
                    entity='user',
                    entity_id=user.id,
                    data=json.dumps({
                        'username': user.username,
                        'role': user.role,
                        'group_id': user.group_id
                    })
                )
                session.add(sync_entry)
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
                sync_entry = SyncQueue(
                    operation='delete',
                    entity='user',
                    entity_id=user_id,
                    data=json.dumps({})
                )
                session.add(sync_entry)
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
                sync_entry = SyncQueue(
                    operation='update',
                    entity='group',
                    entity_id=group.id,
                    data=json.dumps({
                        'name': group.name,
                        'description': group.description,
                        'balance': group.balance
                    })
                )
                session.add(sync_entry)
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
                sync_entry = SyncQueue(
                    operation='delete',
                    entity='group',
                    entity_id=group_id,
                    data=json.dumps({})
                )
                session.add(sync_entry)
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
            session.add(contribution)
            session.flush()
            sync_entry = SyncQueue(
                operation='insert',
                entity='contribution',
                entity_id=contribution.id,
                data=json.dumps({'user_id': str(user_id), 'group_id': str(group_id), 'amount': amount})
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
                if user_id:
                    contribution.user_id = user_id
                if group_id:
                    contribution.group_id = group_id
                if amount is not None:
                    contribution.amount = amount
                session.commit()
                sync_entry = SyncQueue(
                    operation='update',
                    entity='contribution',
                    entity_id=contribution.id,
                    data=json.dumps({
                        'user_id': str(contribution.user_id),
                        'group_id': str(contribution.group_id),
                        'amount': contribution.amount
                    })
                )
                session.add(sync_entry)
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
                session.delete(contribution)
                session.commit()
                sync_entry = SyncQueue(
                    operation='delete',
                    entity='contribution',
                    entity_id=contribution_id,
                    data=json.dumps({})
                )
                session.add(sync_entry)
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
            session.add(loan)
            session.flush()
            sync_entry = SyncQueue(
                operation='insert',
                entity='loan',
                entity_id=loan.id,
                data=json.dumps({
                    'user_id': str(user_id),
                    'group_id': str(group_id),
                    'amount': amount,
                    'interest_rate': interest_rate,
                    'due_date': due_date
                })
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
                session.commit()
                sync_entry = SyncQueue(
                    operation='update',
                    entity='loan',
                    entity_id=loan.id,
                    data=json.dumps({
                        'user_id': str(loan.user_id),
                        'group_id': str(loan.group_id),
                        'amount': loan.amount,
                        'interest_rate': loan.interest_rate,
                        'due_date': loan.due_date.isoformat()
                    })
                )
                session.add(sync_entry)
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
                session.delete(loan)
                session.commit()
                sync_entry = SyncQueue(
                    operation='delete',
                    entity='loan',
                    entity_id=loan_id,
                    data=json.dumps({})
                )
                session.add(sync_entry)
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
            session.add(payout)
            session.flush()
            sync_entry = SyncQueue(
                operation='insert',
                entity='payout',
                entity_id=payout.id,
                data=json.dumps({'group_id': str(group_id), 'user_id': str(user_id), 'amount': amount})
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
                if group_id:
                    payout.group_id = group_id
                if user_id:
                    payout.user_id = user_id
                if amount is not None:
                    payout.amount = amount
                session.commit()
                sync_entry = SyncQueue(
                    operation='update',
                    entity='payout',
                    entity_id=payout.id,
                    data=json.dumps({
                        'group_id': str(payout.group_id),
                        'user_id': str(payout.user_id),
                        'amount': payout.amount
                    })
                )
                session.add(sync_entry)
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
                session.delete(payout)
                session.commit()
                sync_entry = SyncQueue(
                    operation='delete',
                    entity='payout',
                    entity_id=payout_id,
                    data=json.dumps({})
                )
                session.add(sync_entry)
                session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def get_pending_sync_entries(self):
        session = self.Session()
        try:
            entries = session.query(SyncQueue).all()
            return [
                {
                    "id": entry.id,
                    "operation": entry.operation,
                    "entity": entry.entity,
                    "entity_id": entry.entity_id,
                    "data": json.loads(entry.data),
                    "created_at": entry.created_at.isoformat()
                }
                for entry in entries
            ]
        finally:
            session.close()

    def clear_sync_entry(self, sync_id):
        session = self.Session()
        try:
            entry = session.query(SyncQueue).filter_by(id=sync_id).first()
            if entry:
                session.delete(entry)
                session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def get_summary(self):
        session = self.Session()
        try:
            groups = session.query(Group).all()
            loans = session.query(Loan).all()
            summary = {
                'groups': [
                    {'id': g.id, 'name': g.name, 'balance': g.balance}
                    for g in groups
                ],
                'loans': [
                    {'id': l.id, 'user_id': l.user_id, 'amount': l.amount, 'status': l.status}
                    for l in loans
                ]
            }
            return summary
        finally:
            session.close()
