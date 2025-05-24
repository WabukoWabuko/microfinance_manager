from src.database import Database
from PyQt5.QtWidgets import QTableWidgetItem

class RepaymentManager:
    def __init__(self):
        try:
            self.db = Database()
        except Exception as e:
            print(f"Error in RepaymentManager.__init__: {e}")
            raise

    def update_schedule(self, main_ui, user_id):
        try:
            loans = self.db.execute_fetch_all(
                "SELECT id, amount, interest_rate, due_date FROM loans WHERE user_id = ?",
                (str(user_id),)
            )
            main_ui.repayment_table.setRowCount(len(loans))
            for row, loan in enumerate(loans):
                for col, value in enumerate(loan):
                    main_ui.repayment_table.setItem(row, col, QTableWidgetItem(str(value)))
        except Exception as e:
            print(f"Error in update_schedule: {e}")
            raise

    def close(self):
        try:
            self.db.close()
        except Exception as e:
            print(f"Error in close: {e}")
            raise
