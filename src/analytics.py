from src.database import Database

class AnalyticsManager:
    def __init__(self):
        try:
            self.db = Database()
        except Exception as e:
            print(f"Error in AnalyticsManager.__init__: {e}")
            raise

    def update_analytics(self, main_ui, user_id):
        try:
            loans = self.db.execute_fetch_all(
                "SELECT amount, status, interest_rate FROM loans WHERE user_id = ?",
                (str(user_id),)
            )
            total_loans = len(loans)
            total_amount = sum(loan[0] for loan in loans)
            avg_interest = sum(loan[2] for loan in loans) / total_loans if total_loans > 0 else 0
            main_ui.analytics_text.setPlainText(
                f"Total Loans: {total_loans}\nTotal Amount: {total_amount}\nAverage Interest: {avg_interest:.2f}%"
            )
        except Exception as e:
            print(f"Error in update_analytics: {e}")
            raise

    def close(self):
        try:
            self.db.close()
        except Exception as e:
            print(f"Error in close: {e}")
            raise
