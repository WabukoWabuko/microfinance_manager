from src.database import Database

class AuditLogger:
    def __init__(self):
        try:
            self.db = Database()
        except Exception as e:
            print(f"Error in AuditLogger.__init__: {e}")
            raise

    def log_action(self, user_id, action, details):
        try:
            self.db.execute(
                "INSERT INTO AuditLog (user_id, action, details) VALUES (?, ?, ?)",
                (user_id, action, details)
            )
        except Exception as e:
            print(f"Error in log_action: {e}")
            raise

    def close(self):
        try:
            self.db.close()
        except Exception as e:
            print(f"Error in close: {e}")
            raise
