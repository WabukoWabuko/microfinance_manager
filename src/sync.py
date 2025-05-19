import requests
   from decouple import config
   import socket
   from .transactions import TransactionManager

   class SyncManager:
       def __init__(self):
           self.transaction_manager = TransactionManager()
           self.mpesa_api_key = config("MPESA_API_KEY")
           self.mpesa_api_secret = config("MPESA_API_SECRET")
           self.base_url = "https://sandbox.safaricom.co.ke"  # Use production URL for live

       def is_online(self):
           """Check if the app is online."""
           try:
               socket.create_connection(("8.8.8.8", 53), timeout=3)
               return True
           except OSError:
               return False

       def sync_transactions(self):
           """Sync pending transactions with MPesa API."""
           if not self.is_online():
               return False, "No internet connection"

           pending = self.transaction_manager.get_pending_transactions()
           for transaction in pending:
               transaction_id, loan_id, amount, trans_type, date = transaction
               # Placeholder for MPesa API call (to be implemented in Phase 4)
               try:
                   # Simulate MPesa API call
                   response = {"status": "success"}  # Replace with actual API call
                   if response["status"] == "success":
                       self.transaction_manager.mark_synced(transaction_id)
               except requests.RequestException:
                   return False, "Failed to sync transaction"
           return True, "All transactions synced"

       def close(self):
           """Close the transaction manager."""
           self.transaction_manager.close()
