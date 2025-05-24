from datetime import datetime
from src.database import Database
from src.offline import OfflineManager
import uuid
import json

class TransactionManager:
    def __init__(self):
        try:
            self.db = Database()
            self.offline_manager = OfflineManager()
        except Exception as e:
            print(f"Error in TransactionManager.__init__: {e}")
            raise

    def record_transaction(self, loan_id, amount, transaction_type):
        try:
            if not self.offline_manager.is_online():
                transaction_id = str(uuid.uuid4())
                data = {
                    'loan_id': str(loan_id),
                    'amount': amount,
                    'type': transaction_type,
                    'date': datetime.now().isoformat(),
                    'status': 'pending'
                }
                return self.offline_manager.queue_operation("insert", "transactions", transaction_id, json.dumps(data))
            transaction_id = str(uuid.uuid4())
            date = datetime.now().isoformat()
            query = """
                INSERT INTO transactions (id, loan_id, amount, type, date, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            self.db.execute(query, (transaction_id, str(loan_id), amount, transaction_type, date, 'pending'))
            return True, "Transaction recorded"
        except Exception as e:
            print(f"Error in record_transaction: {e}")
            return False, str(e)

    def get_transactions(self, loan_id):
        try:
            query = "SELECT id, loan_id, amount, type FROM transactions WHERE loan_id = ?"
            return self.db.execute_fetch_all(query, (str(loan_id),))
        except Exception as e:
            print(f"Error in get_transactions: {e}")
            raise

    def mark_synced(self, transaction_id):
        try:
            if not self.offline_manager.is_online():
                data = {'status': 'synced'}
                return self.offline_manager.queue_operation("update", "transactions", str(transaction_id), json.dumps(data))
            query = "UPDATE transactions SET status = 'synced' WHERE id = ?"
            self.db.execute(query, (str(transaction_id),))
            return True, "Transaction marked as synced"
        except Exception as e:
            print(f"Error in mark_synced: {e}")
            return False, str(e)

    def get_pending_transactions(self):
        try:
            query = "SELECT id, loan_id, amount, type, date FROM transactions WHERE status = 'pending'"
            return self.db.execute_fetch_all(query)
        except Exception as e:
            print(f"Error in get_pending_transactions: {e}")
            raise

    def close(self):
        try:
            self.db.close()
            self.offline_manager.close()
        except Exception as e:
            print(f"Error in close: {e}")
            raise
