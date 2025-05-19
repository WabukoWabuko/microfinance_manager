from src.database import Database

class AnalyticsManager:
    def __init__(self):
        try:
            self.db = Database()
            print("AnalyticsManager initialized")
        except Exception as e:
            print(f"Error in AnalyticsManager.__init__: {e}")
            raise

    def update_analytics(self, ui, user_id):
        try:
            loans = self.db.fetchall("SELECT * FROM Loans WHERE user_id = ?", (user_id,))
            total_loans = len(loans)
            total_amount = sum(loan[2] for loan in loans)  # amount is column 2
            stats = f"Total Loans: {total_loans}\nTotal Amount: {total_amount:.2f}"
            ui.analytics_text.setPlainText(stats)
            print("Analytics updated")
        except Exception as e:
            print(f"Error in update_analytics: {e}")
            raise

    def close(self):
        try:
            self.db.close()
            print("AnalyticsManager closed")
        except Exception as e:
            print(f"Error in close: {e}")
