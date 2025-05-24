from src.database import Database
import json

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
                data_dict = json.loads(data)
                if entity == "loans" and operation == "insert":
                    query = """
                        INSERT INTO loans (id, user_id, group_id, amount, interest_rate, date_issued, due_date, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    self.db.execute(query, (
                        entity_id,
                        data_dict['user_id'],
                        data_dict.get('group_id'),
                        data_dict['amount'],
                        data_dict['interest_rate'],
                        data_dict['date_issued'],
                        data_dict['due_date'],
                        data_dict['status']
                    ))
                elif entity == "loans" and operation == "update":
                    query = "UPDATE loans SET status = ? WHERE id = ?"
                    self.db.execute(query, (data_dict['status'], entity_id))
                elif entity == "transactions" and operation == "insert":
                    query = """
                        INSERT INTO transactions (id, loan_id, amount, type, date, status)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """
                    self.db.execute(query, (
                        entity_id,
                        data_dict['loan_id'],
                        data_dict['amount'],
                        data_dict['type'],
                        data_dict['date'],
                        data_dict['status']
                    ))
                elif entity == "transactions" and operation == "update":
                    query = "UPDATE transactions SET status = ? WHERE id = ?"
                    self.db.execute(query, (data_dict['status'], entity_id))
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
