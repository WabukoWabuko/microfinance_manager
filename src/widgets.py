from src.database import Database
from PyQt5.QtWidgets import QTableWidgetItem


class WidgetManager:
    def __init__(self):
        try:
            self.db = Database()
        except Exception as e:
            print(f"Error in WidgetManager.__init__: {e}")
            raise

    def setup_dashboard(self, main_ui):
        try:
            main_ui.loan_table.setColumnCount(4)
            main_ui.loan_table.setHorizontalHeaderLabels(
                ["ID", "Amount", "Status", "Issued"])
            main_ui.transaction_table.setColumnCount(4)
            main_ui.transaction_table.setHorizontalHeaderLabels(
                ["ID", "Loan ID", "Amount", "Type"])
        except Exception as e:
            print(f"Error in setup_dashboard: {e}")
            raise

    def update_dashboard(self, main_ui, user_id):
        try:
            loans = self.db.execute_fetch_all(
                "SELECT id, amount, status, date_issued FROM loans WHERE user_id = ?",
                (str(user_id),)
            )
            main_ui.loan_table.setRowCount(len(loans))
            for row, loan in enumerate(loans):
                for col, value in enumerate(loan):
                    main_ui.loan_table.setItem(
                        row, col, QTableWidgetItem(str(value)))
        except Exception as e:
            print(f"Error in update_dashboard: {e}")
            raise

    def close(self):
        try:
            self.db.close()
        except Exception as e:
            print(f"Error in close: {e}")
            raise
