from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
import requests
from local_db import LocalDatabase
from entities import Contribution

class ContributionForm(QDialog):
    def __init__(self, token):
        super().__init__()
        self.setWindowTitle("Add Contribution")
        self.setFixedSize(600, 400)
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

        add_button = QPushButton("Add Contribution")
        add_button.clicked.connect(self.add_contribution)
        layout.addWidget(add_button)

        # Table for displaying contributions
        self.contribution_table = QTableWidget()
        self.contribution_table.setColumnCount(4)
        self.contribution_table.setHorizontalHeaderLabels(["ID", "User ID", "Group ID", "Amount"])
        self.contribution_table.setColumnWidth(0, 150)
        self.contribution_table.setColumnWidth(1, 150)
        self.contribution_table.setColumnWidth(2, 150)
        self.contribution_table.setColumnWidth(3, 100)
        layout.addWidget(QLabel("Contributions:"))
        layout.addWidget(self.contribution_table)

        refresh_button = QPushButton("Refresh Contributions")
        refresh_button.clicked.connect(self.load_contributions)
        layout.addWidget(refresh_button)

        self.setLayout(layout)
        self.load_contributions()

    def add_contribution(self):
        user_id = self.user_id_input.text()
        group_id = self.group_id_input.text()
        amount = self.amount_input.text()

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
            # Validate UUIDs
            import uuid
            uuid.UUID(user_id)
            uuid.UUID(group_id)
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Invalid input: {str(e)}")
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
            self.load_contributions()
            self.user_id_input.clear()
            self.group_id_input.clear()
            self.amount_input.clear()
        except requests.RequestException as e:
            QMessageBox.warning(self, "Warning", f"Added locally, but failed to sync: {str(e)}")
            self.load_contributions()
            self.user_id_input.clear()
            self.group_id_input.clear()
            self.amount_input.clear()

    def load_contributions(self):
        session = self.db.Session()
        try:
            contributions = session.query(Contribution).all()
            self.contribution_table.setRowCount(len(contributions))
            for row, contribution in enumerate(contributions):
                self.contribution_table.setItem(row, 0, QTableWidgetItem(str(contribution.id)))
                self.contribution_table.setItem(row, 1, QTableWidgetItem(str(contribution.user_id)))
                self.contribution_table.setItem(row, 2, QTableWidgetItem(str(contribution.group_id)))
                self.contribution_table.setItem(row, 3, QTableWidgetItem(str(contribution.amount)))
        finally:
            session.close()
