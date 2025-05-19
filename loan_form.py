from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
import requests
from local_db import LocalDatabase
from entities import Loan
from datetime import datetime

class LoanForm(QDialog):
    def __init__(self, token):
        super().__init__()
        self.setWindowTitle("Manage Loans")
        self.setFixedSize(600, 450)
        self.token = token
        self.db = LocalDatabase()

        # Layout and widgets
        layout = QVBoxLayout()

        self.user_id_input = QLineEdit()
        self.user_id_input.setPlaceholderText("User ID (UUID)")
        layout.addWidget(QLabel("User ID:"))
        layout.addWidget(self.user_id_input)

        self.group_id_input = QLineEdit()
        self.group_id_input.setPlaceholderText("Group ID (UUID)")
        layout.addWidget(QLabel("Group ID:"))
        layout.addWidget(self.group_id_input)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")
        layout.addWidget(QLabel("Amount:"))
        layout.addWidget(self.amount_input)

        self.interest_rate_input = QLineEdit()
        self.interest_rate_input.setPlaceholderText("Interest Rate (%)")
        layout.addWidget(QLabel("Interest Rate:"))
        layout.addWidget(self.interest_rate_input)

        self.due_date_input = QLineEdit()
        self.due_date_input.setPlaceholderText("Due Date (YYYY-MM-DD)")
        layout.addWidget(QLabel("Due Date:"))
        layout.addWidget(self.due_date_input)

        add_button = QPushButton("Add Loan")
        add_button.clicked.connect(self.add_loan)
        layout.addWidget(add_button)

        # Table for displaying loans
        self.loan_table = QTableWidget()
        self.loan_table.setColumnCount(5)
        self.loan_table.setHorizontalHeaderLabels(["ID", "User ID", "Group ID", "Amount", "Due Date"])
        self.loan_table.setColumnWidth(0, 150)
        self.loan_table.setColumnWidth(1, 150)
        self.loan_table.setColumnWidth(2, 150)
        self.loan_table.setColumnWidth(3, 100)
        self.loan_table.setColumnWidth(4, 100)
        layout.addWidget(QLabel("Loans:"))
        layout.addWidget(self.loan_table)

        refresh_button = QPushButton("Refresh Loans")
        refresh_button.clicked.connect(self.load_loans)
        layout.addWidget(refresh_button)

        self.setLayout(layout)
        self.load_loans()

    def add_loan(self):
        user_id = self.user_id_input.text()
        group_id = self.group_id_input.text()
        amount = self.amount_input.text()
        interest_rate = self.interest_rate_input.text()
        due_date = self.due_date_input.text()

        try:
            amount = float(amount)
            interest_rate = float(interest_rate)
            if amount <= 0 or interest_rate < 0:
                raise ValueError("Invalid amount or interest rate")
            datetime.fromisoformat(due_date + "T00:00:00")
            import uuid
            uuid.UUID(user_id)
            uuid.UUID(group_id)
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Invalid input: {str(e)}")
            return

        if not all([user_id, group_id, due_date]):
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return

        # Store locally
        try:
            self.db.create_loan(user_id, group_id, amount, interest_rate, due_date + "T00:00:00")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save locally: {str(e)}")
            return

        # Try to save to backend
        try:
            response = requests.post(
                "http://127.0.0.1:8000/loans",
                json={
                    "user_id": user_id,
                    "group_id": group_id,
                    "amount": amount,
                    "interest_rate": interest_rate,
                    "due_date": due_date + "T00:00:00"
                },
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            QMessageBox.information(self, "Success", "Loan added successfully")
            self.load_loans()
            self.user_id_input.clear()
            self.group_id_input.clear()
            self.amount_input.clear()
            self.interest_rate_input.clear()
            self.due_date_input.clear()
        except requests.RequestException as e:
            QMessageBox.warning(self, "Warning", f"Added locally, but failed to sync: {str(e)}")
            self.load_loans()
            self.user_id_input.clear()
            self.group_id_input.clear()
            self.amount_input.clear()
            self.interest_rate_input.clear()
            self.due_date_input.clear()

    def load_loans(self):
        session = self.db.Session()
        try:
            loans = session.query(Loan).all()
            self.loan_table.setRowCount(len(loans))
            for row, loan in enumerate(loans):
                self.loan_table.setItem(row, 0, QTableWidgetItem(str(loan.id)))
                self.loan_table.setItem(row, 1, QTableWidgetItem(str(loan.user_id)))
                self.loan_table.setItem(row, 2, QTableWidgetItem(str(loan.group_id)))
                self.loan_table.setItem(row, 3, QTableWidgetItem(str(loan.amount)))
                self.loan_table.setItem(row, 4, QTableWidgetItem(loan.due_date.strftime("%Y-%m-%d")))
        finally:
            session.close()
