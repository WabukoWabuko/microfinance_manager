from PyQt5.QtWidgets import QTableWidgetItem
from src.database import Database

class RepaymentManager:
    def __init__(self):
        try:
            self.db = Database()
            print("RepaymentManager initialized")
        except Exception as e:
            print(f"Error in RepaymentManager.__init__: {e}")
            raise

    def update_schedule(self, ui, user_id):
        try:
            repayments = self.db.fetchall(
                "SELECT id, loan_id, due_date, amount, status FROM Repayments WHERE loan_id IN (SELECT id FROM Loans WHERE user_id = ?)",
                (user_id,)
            )
            ui.repayment_table.setRowCount(len(repayments))
            ui.repayment_table.setColumnCount(4)
            ui.repayment_table.setHorizontalHeaderLabels(["ID", "Loan ID", "Due Date", "Amount"])
            for row, repayment in enumerate(repayments):
                for col, value in enumerate(repayment[:4]):
                    ui.repayment_table.setItem(row, col, QTableWidgetItem(str(value)))
            ui.repayment_table.resizeColumnsToContents()
            print("Repayment schedule updated")
        except Exception as e:
            print(f"Error in update_schedule: {e}")
            raise

    def add_repayment(self, loan_id, due_date, amount, status="pending"):
        try:
            self.db.execute(
                "INSERT INTO Repayments (loan_id, due_date, amount, status) VALUES (?, ?, ?, ?)",
                (loan_id, due_date, amount, status)
            )
            return True, "Repayment added"
        except Exception as e:
            print(f"Error in add_repayment: {e}")
            return False, str(e)

    def close(self):
        try:
            self.db.close()
            print("RepaymentManager closed")
        except Exception as e:
            print(f"Error in close: {e}")
