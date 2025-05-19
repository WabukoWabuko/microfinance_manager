import socket
from transactions import TransactionManager
from daraja import DarajaAPI

class SyncManager:
   def __init__(self):
       self.transaction_manager = TransactionManager()
       self.daraja_api = DarajaAPI()

   def is_online(self):
       """Check if the app is online."""
       try:
           socket.create_connection(("8.8.8.8", 53), timeout=3)
           return True
       except OSError:
           return False

   def sync_transactions(self):
       """Sync pending transactions with MPesa Daraja API."""
       if not self.is_online():
           return False, "No internet connection"
       pending = self.transaction_manager.get_pending_transactions()
       if not pending:
           return True, "No pending transactions"
       for transaction in pending:
           transaction_id, loan_id, amount, trans_type, date = transaction
           if trans_type == "deposit":
               phone_number = "254700000000"  # Replace with user phone from Users table
               success, result = self.daraja_api.initiate_stk_push(phone_number, amount, transaction_id)
               if success:
                   checkout_request_id = result
                   success, status_msg = self.daraja_api.query_transaction_status(checkout_request_id)
                   if success:
                       self.transaction_manager.mark_synced(transaction_id)
                   else:
                       return False, status_msg
               else:
                   return False, result
           else:
               # Handle withdrawals (e.g., B2C API, to be implemented)
               return False, "Withdrawal syncing not implemented"
       return True, "All transactions synced"

   def close(self):
       """Close the transaction manager."""
       self.transaction_manager.close()
