from src.database import Database
     import uuid
     import requests

     class OfflineManager:
         def __init__(self):
             try:
                 self.db = Database()
             except Exception as e:
                 print(f"Error in OfflineManager.__init__: {e}")
                 raise

         def sync_if_online(self, sync_function):
             try:
                 if self.is_online():
                     return sync_function()
                 else:
                     return False, "Offline: Operation queued"
             except Exception as e:
                 print(f"Error in sync_if_online: {e}")
                 return False, str(e)

         def queue_operation(self, operation, entity, entity_id, data):
             try:
                 queue_id = str(uuid.uuid4())
                 query = """
                     INSERT INTO sync_queue (id, operation, entity, entity_id, data, created_at)
                     VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                 """
                 self.db.execute(query, (queue_id, operation, entity, entity_id, data))
                 return True, "Operation queued"
             except Exception as e:
                 print(f"Error in queue_operation: {e}")
                 return False, str(e)

         def is_online(self):
             try:
                 requests.get("https://www.google.com", timeout=5)
                 return True
             except requests.ConnectionError:
                 return False

         def close(self):
             try:
                 self.db.close()
             except Exception as e:
                 print(f"Error in close: {e}")
                 raise
