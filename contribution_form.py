from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import requests
from local_db import LocalDatabase

class ContributionForm(QDialog):
    def __init__(self, token):
        super().__init__()
        self.setWindowTitle("Add Contribution")
        self.setFixedSize(300, 250)
        self.token = token
        self.db = LocalDatabase()

        # Layout and widgets
        layout = QVBoxLayout()

        self.user_id_input = QLineEdit()
        self.user_id_input.setPlaceholderText("User ID")
        layout.addWidget(QLabel("User ID:"))
        layout.addWidget(self.user_id_input)

        self.group_id_input = QLineEdit()
        self.group_id_input.setPlaceholderText("Group ID")
        layout.addWidget(QLabel("Group ID:"))
        layout.addWidget(self.group_id_input)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")
        layout.addWidget(QLabel("Amount:"))
        layout.addWidget(self.amount_input)

        add_button = QPushButton("Add Contribution")
        add_button.clicked.connect(self.add_contribution)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_contribution(self):
        user_id = self.user_id_input.text()
        group_id = self.group_id_input.text()
        amount = self.amount_input.text()

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Invalid amount: {str(e)}")
            return

        if not all([user_id, group_id]):
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return

        # Store locally
        try:
            self.db.create_contribution(user_id, group_id, amount)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save locally: {str(e)}")
            return

        # Try to save to backend
        try:
            response = requests.post(
                "http://127.0.0.1:8000/contributions",
                json={"user_id": user_id, "group_id": group_id, "amount": amount},
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            QMessageBox.information(self, "Success", "Contribution added successfully")
            self.accept()
        except requests.RequestException as e:
            QMessageBox.warning(self, "Warning", f"Added locally, but failed to sync: {str(e)}")
            self.accept()
