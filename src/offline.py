from datetime import datetime
from src.database import Database

class OfflineManager:
    def __init__(self):
        try:
            self.db = Database()
            print("OfflineManager initialized")
        except Exception as e:
            print(f"Error in OfflineManager.__init__: {e}")
            raise

    def sync_if_online(self, sync_func):
        try:
            return sync_func()
        except Exception as e:
            self.db.execute("INSERT INTO OfflineCache (action, data, created_at) VALUES (?, ?, ?)",
                            ("sync", "pending", datetime.now()))
            print(f"Error in sync_if_online, cached: {e}")
            return False, "Cached for later sync"

    def close(self):
        try:
            self.db.close()
            print("OfflineManager closed")
        except Exception as e:
            print(f"Error in close: {e}")
