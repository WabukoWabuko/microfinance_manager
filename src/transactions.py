from datetime import datetime
from src.database import Database

class TransactionManager:
   def __init__(self):
       self.db = Database()

   def record_transaction(self, loan_id, amount, transaction_type):
       """Record a deposit or withdrawal."""
       date = datetime.now().isoformat()
       query = """
           INSERT INTO Transactions (loan_id, amount, type, date, sync_status)
           VALUES (?, ?, ?, ?, 'pending')
       """
       self.db.execute(query, (loan_id, amount, transaction_type, date))
       return True, "Transaction recorded"

   def get_transactions(self, loan_id):
       """Retrieve all transactions for a loan."""
       query = "SELECT id, amount, type, date, sync_status FROM Transactions WHERE loan_id = ?"
       return self.db.fetch_all(query, (loan_id,))

   def mark_synced(self, transaction_id):
       """Mark a transaction as synced."""
       query = "UPDATE Transactions SET sync_status = 'synced' WHERE id = ?"
       self.db.execute(query, (transaction_id,))
       return True, "Transaction marked as synced"

   def get_pending_transactions(self):
       """Retrieve all pending transactions for sync."""
       query = "SELECT id, loan_id, amount, type, date FROM Transactions WHERE sync_status = 'pending'"
       return self.db.fetch_all(query)

   def close(self):
       """Close the database connection."""
       self.db.close()
