from datetime import datetime
from src.database import Database

class NotificationManager:
    def __init__(self):
        try:
            self.db = Database()
            print("NotificationManager initialized")
        except Exception as e:
            print(f"Error in NotificationManager.__init__: {e}")
            raise

    def check_due_payments(self, user):
        try:
            if user:
                due = self.db.fetchall("SELECT * FROM Repayments WHERE status = 'pending' AND due_date < ? AND loan_id IN (SELECT id FROM Loans WHERE user_id = ?)",
                                       (datetime.now(), user["id"]))
                for d in due:
                    self.db.execute("INSERT INTO Notifications (user_id, message, created_at) VALUES (?, ?, ?)",
                                    (user["id"], f"Payment due: {d[3]:.2f} on {d[2]}", datetime.now()))
                print("Checked due payments")
        except Exception as e:
            print(f"Error in check_due_payments: {e}")
            raise

    def get_notifications(self, user_id):
        try:
            notifications = self.db.fetchall("SELECT * FROM Notifications WHERE user_id = ?", (user_id,))
            return [{"message": n[2], "created_at": n[3]} for n in notifications]
        except Exception as e:
            print(f"Error in get_notifications: {e}")
            return []

    def close(self):
        try:
            self.db.close()
            print("NotificationManager closed")
        except Exception as e:
            print(f"Error in close: {e}")
