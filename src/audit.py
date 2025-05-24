from src.database import Database
import uuid


class AuditLogger:
    def __init__(self):
        try:
            self.db = Database()
        except Exception as e:
            print(f"Error in AuditLogger.__init__: {e}")
            raise

    def log_action(self, user_id, action, details):
        try:
            audit_id = str(uuid.uuid4())
            query = """
                INSERT INTO AuditLog (id, user_id, action, details)
                VALUES (?, ?, ?, ?)
            """
            self.db.execute(query, (audit_id, str(user_id)
                            if user_id else None, action, details))
        except Exception as e:
            print(f"Error in log_action: {e}")
            raise

    def close(self):
        try:
            self.db.close()
        except Exception as e:
            print(f"Error in close: {e}")
            raise
