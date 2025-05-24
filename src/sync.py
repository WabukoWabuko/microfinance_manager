from src.database import Database

     class SyncManager:
         def __init__(self):
             try:
                 self.db = Database()
             except Exception as e:
                 print(f"Error in SyncManager.__init__: {e}")
                 raise

         def sync_transactions(self):
             try:
                 queued = self.db.execute_fetch_all(
                     "SELECT id, operation, entity, entity_id, data FROM sync_queue"
                 )
                 for queue_id, operation, entity, entity_id, data in queued:
                     if entity == "loans":
                         query = """
                             INSERT INTO loans (id, user_id, group_id, amount, interest_rate, date_issued, due_date, status)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                         """
                         self.db.execute(query, (entity_id, data['user_id'], None, data['amount'], data['interest_rate'], data['date_issued'], data['due_date'], 'pending'))
                     self.db.execute("DELETE FROM sync_queue WHERE id = ?", (queue_id,))
                 return True, "Sync completed"
             except Exception as e:
                 print(f"Error in sync_transactions: {e}")
                 return False, str(e)

         def close(self):
             try:
                 self.db.close()
             except Exception as e:
                 print(f"Error in close: {e}")
                 raise
