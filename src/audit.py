from datetime import datetime
from src.database import Database

class AuditLogger:
    def __init__(self):
        try:
            self.db = Database()
            print("AuditLogger initialized")
        except Exception as e:
            print(f"Error in AuditLogger.__init__: {e}")
            raise

    def log_action(self, user_id, action, details):
        try:
            self.db.execute("INSERT INTO AuditLogs (user_id, action, details, timestamp) VALUES (?, ?, ?, ?)",
                            (user_id, action, details, datetime.now()))
            print(f"Logged action: {action}")
        except Exception as e:
            print(f"Error in log_action: {e}")
            raise

    def close(self):
        try:
            self.db.close()
            print("AuditLogger closed")
        except Exception as e:
            print(f"Error in close: {e}")
