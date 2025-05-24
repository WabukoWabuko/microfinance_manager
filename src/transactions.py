from datetime import datetime
from src.database import Database
import uuid

class TransactionManager:
    def __init__(self):
        try:
            self.db = Database()
        except Exception as e:
            print(f"Error in TransactionManager.__init__: {e}")
            raise

    def record_transaction(self, loan_id, amount, transaction_type):
        try:
            transaction_id = str(uuid.uuid4())
            date = datetime.now().isoformat()
            query = """
                INSERT INTO transactions (id, loan_id, amount, type, date, status)
                VALUES (?, ?, ?, ?, ?, 'pending')
            """
            self.db.execute(query, (transaction_id, str(loan_id), amount, transaction_type, date))
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
        except Exception as e:
            print(f"Error in close: {e}")
            raise
