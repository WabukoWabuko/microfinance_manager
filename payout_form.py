from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
import requests
from local_db import LocalDatabase

class PayoutForm(QDialog):
    def __init__(self, token):
        super().__init__()
        self.setWindowTitle("Manage Payouts")
        self.setFixedSize(600, 400)
        self.token = token
        self.db = LocalDatabase()

        # Layout and widgets
        layout = QVBoxLayout()

        self.group_id_input = QLineEdit()
        self.group_id_input.setPlaceholderText("Group ID (UUID)")
        layout.addWidget(QLabel("Group ID:"))
        layout.addWidget(self.group_id_input)

        self.user_id_input = QLineEdit()
        self.user_id_input.setPlaceholderText("User ID (UUID)")
        layout.addWidget(QLabel("User ID:"))
        layout.addWidget(self.user_id_input)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")
        layout.addWidget(QLabel("Amount:"))
        layout.addWidget(self.amount_input)

        add_button = QPushButton("Add Payout")
        add_button.clicked.connect(self.add_payout)
        layout.addWidget(add_button)

        # Table for displaying payouts
        self.payout_table = QTableWidget()
        self.payout_table.setColumnCount(4)
        self.payout_table.setHorizontalHeaderLabels(["ID", "Group ID", "User ID", "Amount"])
        self.payout_table.setColumnWidth(0, 150)
        self.payout_table.setColumnWidth(1, 150)
        self.payout_table.setColumnWidth(2, 150)
        self.payout_table.setColumnWidth(3, 100)
        layout.addWidget(QLabel("Payouts:"))
        layout.addWidget(self.payout_table)

        refresh_button = QPushButton("Refresh Payouts")
        refresh_button.clicked.connect(self.load_payouts)
        layout.addWidget(refresh_button)

        self.setLayout(layout)
        self.load_payouts()

    def add_payout(self):
        group_id = self.group_id_input.text()
        user_id = self.user_id_input.text()
        amount = self.amount_input.text()

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
            import uuid
            uuid.UUID(group_id)
            uuid.UUID(user_id)
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Invalid input: {str(e)}")
            return

        if not all([group_id, user_id]):
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return

        # Store locally
        try:
            self.db.create_payout(group_id, user_id, amount)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save locally: {str(e)}")
            return

        # Try to save to backend
        try:
            response = requests.post(
                "http://127.0.0.1:8000/payouts",
                json={"group_id": group_id, "user_id": user_id, "amount": amount},
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            QMessageBox.information(self, "Success", "Payout added successfully")
            self.load_payouts()
            self.group_id_input.clear()
            self.user_id_input.clear()
            self.amount_input.clear()
        except requests.RequestException as e:
            QMessageBox.warning(self, "Warning", f"Added locally, but failed to sync: {str(e)}")
            self.load_payouts()
            self.group_id_input.clear()
            self.user_id_input.clear()
            self.amount_input.clear()

    def load_payouts(self):
        session = self.db.Session()
        try:
            payouts = session.query(self.db.Payout).all()
            self.payout_table.setRowCount(len(payouts))
            for row, payout in enumerate(payouts):
                self.payout_table.setItem(row, 0, QTableWidgetItem(str(payout.id)))
                self.payout_table.setItem(row, 1, QTableWidgetItem(str(payout.group_id)))
                self.payout_table.setItem(row, 2, QTableWidgetItem(str(payout.user_id)))
                self.payout_table.setItem(row, 3, QTableWidgetItem(str(payout.amount)))
        finally:
            session.close()
