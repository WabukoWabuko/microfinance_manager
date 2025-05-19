from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QTextEdit, QMessageBox, QHBoxLayout
from PyQt6.QtCore import Qt
import requests
from local_db import LocalDatabase
from entities import User, Group, Contribution, Loan, Payout
from datetime import datetime
import json

class MainWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()
        self.setWindowTitle("Microfinance Manager")
        self.setFixedSize(800, 600)
        self.token = token
        self.db = LocalDatabase()

        # Main widget and layout
        widget = QWidget()
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # User Tab
        self.user_widget = QWidget()
        self.user_layout = QVBoxLayout()
        self.setup_user_tab()
        self.user_widget.setLayout(self.user_layout)
        self.tabs.addTab(self.user_widget, "Users")

        # Group Tab
        self.group_widget = QWidget()
        self.group_layout = QVBoxLayout()
        self.setup_group_tab()
        self.group_widget.setLayout(self.group_layout)
        self.tabs.addTab(self.group_widget, "Groups")

        # Contribution Tab
        self.contribution_widget = QWidget()
        self.contribution_layout = QVBoxLayout()
        self.setup_contribution_tab()
        self.contribution_widget.setLayout(self.contribution_layout)
        self.tabs.addTab(self.contribution_widget, "Contributions")

        # Loan Tab
        self.loan_widget = QWidget()
        self.loan_layout = QVBoxLayout()
        self.setup_loan_tab()
        self.loan_widget.setLayout(self.loan_layout)
        self.tabs.addTab(self.loan_widget, "Loans")

        # Payout Tab
        self.payout_widget = QWidget()
        self.payout_layout = QVBoxLayout()
        self.setup_payout_tab()
        self.payout_widget.setLayout(self.payout_layout)
        self.tabs.addTab(self.payout_widget, "Payouts")

        # Summary Tab
        self.summary_widget = QWidget()
        self.summary_layout = QVBoxLayout()
        self.setup_summary_tab()
        self.summary_widget.setLayout(self.summary_layout)
        self.tabs.addTab(self.summary_widget, "Summary")

        # Sync Tab
        self.sync_widget = QWidget()
        self.sync_layout = QVBoxLayout()
        self.setup_sync_tab()
        self.sync_widget.setLayout(self.sync_layout)
        self.tabs.addTab(self.sync_widget, "Sync")

        layout.addWidget(self.tabs)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Apply stylesheet
        self.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #444; background: #f5f5f5; }
            QTabBar::tab { background: #333; color: white; padding: 8px; font-weight: bold; }
            QTabBar::tab:selected { background: #4CAF50; }
            QPushButton { background: #4CAF50; color: white; padding: 5px; border-radius: 3px; }
            QPushButton:hover { background: #45a049; }
            QLineEdit, QComboBox { border: 1px solid #444; padding: 3px; background: white; }
            QTableWidget { gridline-color: #444; background: white; }
            QTextEdit { border: 1px solid #444; background: white; }
        """)

    def setup_user_tab(self):
        form_layout = QFormLayout()
        self.user_username = QLineEdit()
        self.user_password = QLineEdit()
        self.user_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.user_role = QLineEdit()
        form_layout.addRow("Username:", self.user_username)
        form_layout.addRow("Password:", self.user_password)
        form_layout.addRow("Role:", self.user_role)

        button_layout = QHBoxLayout()
        create_btn = QPushButton("Create User")
        create_btn.clicked.connect(self.create_user)
        update_btn = QPushButton("Update User")
        update_btn.clicked.connect(self.update_user)
        button_layout.addWidget(create_btn)
        button_layout.addWidget(update_btn)

        self.user_table = QTableWidget()
        self.user_table.setColumnCount(4)
        self.user_table.setHorizontalHeaderLabels(["ID", "Username", "Role", "Actions"])
        self.user_table.setColumnWidth(0, 200)
        self.user_table.setColumnWidth(1, 150)
        self.user_table.setColumnWidth(2, 100)
        self.user_table.setColumnWidth(3, 100)
        self.user_table.cellClicked.connect(self.select_user)

        self.user_layout.addLayout(form_layout)
        self.user_layout.addLayout(button_layout)
        self.user_layout.addWidget(self.user_table)
        self.load_users()

    def setup_group_tab(self):
        form_layout = QFormLayout()
        self.group_name = QLineEdit()
        self.group_description = QLineEdit()
        form_layout.addRow("Name:", self.group_name)
        form_layout.addRow("Description:", self.group_description)

        button_layout = QHBoxLayout()
        create_btn = QPushButton("Create Group")
        create_btn.clicked.connect(self.create_group)
        update_btn = QPushButton("Update Group")
        update_btn.clicked.connect(self.update_group)
        button_layout.addWidget(create_btn)
        button_layout.addWidget(update_btn)

        self.group_table = QTableWidget()
        self.group_table.setColumnCount(4)
        self.group_table.setHorizontalHeaderLabels(["ID", "Name", "Balance", "Actions"])
        self.group_table.setColumnWidth(0, 200)
        self.group_table.setColumnWidth(1, 150)
        self.group_table.setColumnWidth(2, 100)
        self.group_table.setColumnWidth(3, 100)
        self.group_table.cellClicked.connect(self.select_group)

        self.group_layout.addLayout(form_layout)
        self.group_layout.addLayout(button_layout)
        self.group_layout.addWidget(self.group_table)
        self.load_groups()

    def setup_contribution_tab(self):
        form_layout = QFormLayout()
        self.contribution_user_id = QComboBox()
        self.contribution_group_id = QComboBox()
        self.contribution_amount = QLineEdit()
        form_layout.addRow("User:", self.contribution_user_id)
        form_layout.addRow("Group:", self.contribution_group_id)
        form_layout.addRow("Amount:", self.contribution_amount)
        self.populate_user_dropdown(self.contribution_user_id)
        self.populate_group_dropdown(self.contribution_group_id)

        button_layout = QHBoxLayout()
        create_btn = QPushButton("Create Contribution")
        create_btn.clicked.connect(self.create_contribution)
        update_btn = QPushButton("Update Contribution")
        update_btn.clicked.connect(self.update_contribution)
        button_layout.addWidget(create_btn)
        button_layout.addWidget(update_btn)

        self.contribution_table = QTableWidget()
        self.contribution_table.setColumnCount(5)
        self.contribution_table.setHorizontalHeaderLabels(["ID", "User ID", "Group ID", "Amount", "Actions"])
        self.contribution_table.setColumnWidth(0, 150)
        self.contribution_table.setColumnWidth(1, 150)
        self.contribution_table.setColumnWidth(2, 150)
        self.contribution_table.setColumnWidth(3, 100)
        self.contribution_table.setColumnWidth(4, 100)
        self.contribution_table.cellClicked.connect(self.select_contribution)

        self.contribution_layout.addLayout(form_layout)
        self.contribution_layout.addLayout(button_layout)
        self.contribution_layout.addWidget(self.contribution_table)
        self.load_contributions()

    def setup_loan_tab(self):
        form_layout = QFormLayout()
        self.loan_user_id = QComboBox()
        self.loan_group_id = QComboBox()
        self.loan_amount = QLineEdit()
        self.loan_interest_rate = QLineEdit()
        self.loan_due_date = QLineEdit()
        self.loan_due_date.setPlaceholderText("YYYY-MM-DD")
        form_layout.addRow("User:", self.loan_user_id)
        form_layout.addRow("Group:", self.loan_group_id)
        form_layout.addRow("Amount:", self.loan_amount)
        form_layout.addRow("Interest Rate (%):", self.loan_interest_rate)
        form_layout.addRow("Due Date:", self.loan_due_date)
        self.populate_user_dropdown(self.loan_user_id)
        self.populate_group_dropdown(self.loan_group_id)

        button_layout = QHBoxLayout()
        create_btn = QPushButton("Create Loan")
        create_btn.clicked.connect(self.create_loan)
        update_btn = QPushButton("Update Loan")
        update_btn.clicked.connect(self.update_loan)
        button_layout.addWidget(create_btn)
        button_layout.addWidget(update_btn)

        self.loan_table = QTableWidget()
        self.loan_table.setColumnCount(6)
        self.loan_table.setHorizontalHeaderLabels(["ID", "User ID", "Group ID", "Amount", "Due Date", "Actions"])
        self.loan_table.setColumnWidth(0, 150)
        self.loan_table.setColumnWidth(1, 150)
        self.loan_table.setColumnWidth(2, 150)
        self.loan_table.setColumnWidth(3, 100)
        self.loan_table.setColumnWidth(4, 100)
        self.loan_table.setColumnWidth(5, 100)
        self.loan_table.cellClicked.connect(self.select_loan)

        self.loan_layout.addLayout(form_layout)
        self.loan_layout.addLayout(button_layout)
        self.loan_layout.addWidget(self.loan_table)
        self.load_loans()

    def setup_payout_tab(self):
        form_layout = QFormLayout()
        self.payout_group_id = QComboBox()
        self.payout_user_id = QComboBox()
        self.payout_amount = QLineEdit()
        form_layout.addRow("Group:", self.payout_group_id)
        form_layout.addRow("User:", self.payout_user_id)
        form_layout.addRow("Amount:", self.payout_amount)
        self.populate_group_dropdown(self.payout_group_id)
        self.populate_user_dropdown(self.payout_user_id)

        button_layout = QHBoxLayout()
        create_btn = QPushButton("Create Payout")
        create_btn.clicked.connect(self.create_payout)
        update_btn = QPushButton("Update Payout")
        update_btn.clicked.connect(self.update_payout)
        button_layout.addWidget(create_btn)
        button_layout.addWidget(update_btn)

        self.payout_table = QTableWidget()
        self.payout_table.setColumnCount(5)
        self.payout_table.setHorizontalHeaderLabels(["ID", "Group ID", "User ID", "Amount", "Actions"])
        self.payout_table.setColumnWidth(0, 150)
        self.payout_table.setColumnWidth(1, 150)
        self.payout_table.setColumnWidth(2, 150)
        self.payout_table.setColumnWidth(3, 100)
        self.payout_table.setColumnWidth(4, 100)
        self.payout_table.cellClicked.connect(self.select_payout)

        self.payout_layout.addLayout(form_layout)
        self.payout_layout.addLayout(button_layout)
        self.payout_layout.addWidget(self.payout_table)
        self.load_payouts()

    def setup_summary_tab(self):
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        refresh_btn = QPushButton("Refresh Summary")
        refresh_btn.clicked.connect(self.load_summary)
        self.summary_layout.addWidget(self.summary_text)
        self.summary_layout.addWidget(refresh_btn)
        self.load_summary()

    def setup_sync_tab(self):
        self.sync_text = QTextEdit()
        self.sync_text.setReadOnly(True)
        sync_btn = QPushButton("Sync Now")
        sync_btn.clicked.connect(self.perform_sync)
        self.sync_layout.addWidget(self.sync_text)
        self.sync_layout.addWidget(sync_btn)

    def populate_user_dropdown(self, combo_box):
        combo_box.clear()
        users = self.db.get_all_users()
        for user in users:
            combo_box.addItem(f"{user.username} ({user.id[:8]}...)", user.id)

    def populate_group_dropdown(self, combo_box):
        combo_box.clear()
        groups = self.db.get_all_groups()
        for group in groups:
            combo_box.addItem(f"{group.name} ({group.id[:8]}...)", group.id)

    def create_user(self):
        username = self.user_username.text()
        password = self.user_password.text()
        role = self.user_role.text()
        if not all([username, password, role]):
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return
        try:
            response = requests.post(
                "http://127.0.0.1:8000/users",
                json={"username": username, "password": password, "role": role},
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            self.db.create_user(username, password, role)
            QMessageBox.information(self, "Success", "User created")
            self.load_users()
            self.user_username.clear()
            self.user_password.clear()
            self.user_role.clear()
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to create user: {str(e)}")

    def select_user(self, row, column):
        if column == 3:
            user_id = self.user_table.item(row, 0).text()
            action = self.user_table.item(row, 3).text()
            if action == "Delete":
                self.delete_user(user_id)
            return
        self.user_username.setText(self.user_table.item(row, 1).text())
        self.user_role.setText(self.user_table.item(row, 2).text())

    def update_user(self):
        username = self.user_username.text()
        password = self.user_password.text()
        role = self.user_role.text()
        selected_row = self.user_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Select a user to update")
            return
        user_id = self.user_table.item(selected_row, 0).text()
        if not all([username, role]):
            QMessageBox.warning(self, "Error", "Username and role are required")
            return
        try:
            json_data = {"username": username, "role": role}
            if password:
                json_data["password"] = password
            else:
                json_data["password"] = "unchanged"
            response = requests.put(
                f"http://127.0.0.1:8000/users/{user_id}",
                json=json_data,
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            self.db.update_user(user_id, username, password or None, role)
            QMessageBox.information(self, "Success", "User updated")
            self.load_users()
            self.user_username.clear()
            self.user_password.clear()
            self.user_role.clear()
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to update user: {str(e)}")

    def delete_user(self, user_id):
        reply = QMessageBox.question(self, "Confirm", "Delete this user?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return
        try:
            response = requests.delete(
                f"http://127.0.0.1:8000/users/{user_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            self.db.delete_user(user_id)
            QMessageBox.information(self, "Success", "User deleted")
            self.load_users()
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to delete user: {str(e)}")

    def create_group(self):
        name = self.group_name.text()
        description = self.group_description.text() or None
        if not name:
            QMessageBox.warning(self, "Error", "Please enter a group name")
            return
        try:
            response = requests.post(
                "http://127.0.0.1:8000/groups",
                json={"name": name, "description": description, "balance": 0.0},
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            self.db.create_group(name, description)
            QMessageBox.information(self, "Success", "Group created")
            self.load_groups()
            self.group_name.clear()
            self.group_description.clear()
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to create group: {str(e)}")

    def select_group(self, row, column):
        if column == 3:
            group_id = self.group_table.item(row, 0).text()
            action = self.group_table.item(row, 3).text()
            if action == "Delete":
                self.delete_group(group_id)
            return
        self.group_name.setText(self.group_table.item(row, 1).text())
        self.group_description.setText(self.group_table.item(row, 2).text())

    def update_group(self):
        name = self.group_name.text()
        description = self.group_description.text() or None
        selected_row = self.group_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Select a group to update")
            return
        group_id = self.group_table.item(selected_row, 0).text()
        if not name:
            QMessageBox.warning(self, "Error", "Group name is required")
            return
        try:
            response = requests.put(
                f"http://127.0.0.1:8000/groups/{group_id}",
                json={"name": name, "description": description, "balance": 0.0},
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            self.db.update_group(group_id, name, description)
            QMessageBox.information(self, "Success", "Group updated")
            self.load_groups()
            self.group_name.clear()
            self.group_description.clear()
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to update group: {str(e)}")

    def delete_group(self, group_id):
        reply = QMessageBox.question(self, "Confirm", "Delete this group?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return
        try:
            response = requests.delete(
                f"http://127.0.0.1:8000/groups/{group_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            self.db.delete_group(group_id)
            QMessageBox.information(self, "Success", "Group deleted")
            self.load_groups()
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to delete group: {str(e)}")

    def create_contribution(self):
        user_id = self.contribution_user_id.currentData()
        group_id = self.contribution_group_id.currentData()
        amount = self.contribution_amount.text()
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Invalid amount: {str(e)}")
            return
        if not all([user_id, group_id]):
            QMessageBox.warning(self, "Error", "Please select user and group")
            return
        try:
            self.db.create_contribution(user_id, group_id, amount)
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/contributions",
                    json={"user_id": str(user_id), "group_id": str(group_id), "amount": amount},
                    headers={"Authorization": f"Bearer {self.token}"}
                )
                response.raise_for_status()
                QMessageBox.information(self, "Success", "Contribution created")
            except requests.RequestException as e:
                QMessageBox.warning(self, "Warning", f"Added locally, failed to sync: {str(e)}")
            self.load_contributions()
            self.contribution_amount.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create contribution: {str(e)}")

    def select_contribution(self, row, column):
        if column == 4:
            contribution_id = self.contribution_table.item(row, 0).text()
            action = self.contribution_table.item(row, 4).text()
            if action == "Delete":
                self.delete_contribution(contribution_id)
            return
        user_id = self.contribution_table.item(row, 1).text()
        group_id = self.contribution_table.item(row, 2).text()
        self.contribution_user_id.setCurrentIndex(
            self.contribution_user_id.findData(user_id) if user_id else -1
        )
        self.contribution_group_id.setCurrentIndex(
            self.contribution_group_id.findData(group_id) if group_id else -1
        )
        self.contribution_amount.setText(self.contribution_table.item(row, 3).text())

    def update_contribution(self):
        user_id = self.contribution_user_id.currentData()
        group_id = self.contribution_group_id.currentData()
        amount = self.contribution_amount.text()
        selected_row = self.contribution_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Select a contribution to update")
            return
        contribution_id = self.contribution_table.item(selected_row, 0).text()
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
            if not all([user_id, group_id]):
                raise ValueError("User and group are required")
            response = requests.put(
                f"http://127.0.0.1:8000/contributions/{contribution_id}",
                json={"user_id": str(user_id), "group_id": str(group_id), "amount": amount},
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            self.db.update_contribution(contribution_id, user_id, group_id, amount)
            QMessageBox.information(self, "Success", "Contribution updated")
            self.load_contributions()
            self.contribution_amount.clear()
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Invalid input: {str(e)}")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to update contribution: {str(e)}")

    def delete_contribution(self, contribution_id):
        reply = QMessageBox.question(self, "Confirm", "Delete this contribution?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return
        try:
            response = requests.delete(
                f"http://127.0.0.1:8000/contributions/{contribution_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            self.db.delete_contribution(contribution_id)
            QMessageBox.information(self, "Success", "Contribution deleted")
            self.load_contributions()
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to delete contribution: {str(e)}")

    def create_loan(self):
        user_id = self.loan_user_id.currentData()
        group_id = self.loan_group_id.currentData()
        amount = self.loan_amount.text()
        interest_rate = self.loan_interest_rate.text()
        due_date = self.loan_due_date.text()
        try:
            amount = float(amount)
            interest_rate = float(interest_rate)
            if amount <= 0 or interest_rate < 0:
                raise ValueError("Invalid amount or interest rate")
            datetime.fromisoformat(due_date + "T00:00:00")
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Invalid input: {str(e)}")
            return
        if not all([user_id, group_id, due_date]):
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return
        try:
            self.db.create_loan(user_id, group_id, amount, interest_rate, due_date + "T00:00:00")
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/loans",
                    json={
                        "user_id": str(user_id),
                        "group_id": str(group_id),
                        "amount": amount,
                        "interest_rate": interest_rate,
                        "due_date": due_date + "T00:00:00"
                    },
                    headers={"Authorization": f"Bearer {self.token}"}
                )
                response.raise_for_status()
                QMessageBox.information(self, "Success", "Loan created")
            except requests.RequestException as e:
                QMessageBox.warning(self, "Warning", f"Added locally, failed to sync: {str(e)}")
            self.load_loans()
            self.loan_amount.clear()
            self.loan_interest_rate.clear()
            self.loan_due_date.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create loan: {str(e)}")

    def select_loan(self, row, column):
        if column == 5:
            loan_id = self.loan_table.item(row, 0).text()
            action = self.loan_table.item(row, 5).text()
            if action == "Delete":
                self.delete_loan(loan_id)
            return
        user_id = self.loan_table.item(row, 1).text()
        group_id = self.loan_table.item(row, 2).text()
        self.loan_user_id.setCurrentIndex(
            self.loan_user_id.findData(user_id) if user_id else -1
        )
        self.loan_group_id.setCurrentIndex(
            self.loan_group_id.findData(group_id) if group_id else -1
        )
        self.loan_amount.setText(self.loan_table.item(row, 3).text())
        self.loan_due_date.setText(self.loan_table.item(row, 4).text())

    def update_loan(self):
        user_id = self.loan_user_id.currentData()
        group_id = self.loan_group_id.currentData()
        amount = self.loan_amount.text()
        interest_rate = self.loan_interest_rate.text()
        due_date = self.loan_due_date.text()
        selected_row = self.loan_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Select a loan to update")
            return
        loan_id = self.loan_table.item(selected_row, 0).text()
        try:
            amount = float(amount)
            interest_rate = float(interest_rate)
            if amount <= 0 or interest_rate < 0:
                raise ValueError("Invalid amount or interest rate")
            datetime.fromisoformat(due_date + "T00:00:00")
            if not all([user_id, group_id, due_date]):
                raise ValueError("All fields are required")
            response = requests.put(
                f"http://127.0.0.1:8000/loans/{loan_id}",
                json={
                    "user_id": str(user_id),
                    "group_id": str(group_id),
                    "amount": amount,
                    "interest_rate": interest_rate,
                    "due_date": due_date + "T00:00:00"
                },
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            self.db.update_loan(loan_id, user_id, group_id, amount, interest_rate, due_date + "T00:00:00")
            QMessageBox.information(self, "Success", "Loan updated")
            self.load_loans()
            self.loan_amount.clear()
            self.loan_interest_rate.clear()
            self.loan_due_date.clear()
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Invalid input: {str(e)}")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to update loan: {str(e)}")

    def delete_loan(self, loan_id):
        reply = QMessageBox.question(self, "Confirm", "Delete this loan?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return
        try:
            response = requests.delete(
                f"http://127.0.0.1:8000/loans/{loan_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            self.db.delete_loan(loan_id)
            QMessageBox.information(self, "Success", "Loan deleted")
            self.load_loans()
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to delete loan: {str(e)}")

    def create_payout(self):
        group_id = self.payout_group_id.currentData()
        user_id = self.payout_user_id.currentData()
        amount = self.payout_amount.text()
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Invalid amount: {str(e)}")
            return
        if not all([group_id, user_id]):
            QMessageBox.warning(self, "Error", "Please select group and user")
            return
        try:
            self.db.create_payout(group_id, user_id, amount)
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/payouts",
                    json={"group_id": str(group_id), "user_id": str(user_id), "amount": amount},
                    headers={"Authorization": f"Bearer {self.token}"}
                )
                response.raise_for_status()
                QMessageBox.information(self, "Success", "Payout created")
            except requests.RequestException as e:
                QMessageBox.warning(self, "Warning", f"Added locally, failed to sync: {str(e)}")
            self.load_payouts()
            self.payout_amount.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create payout: {str(e)}")

    def select_payout(self, row, column):
        if column == 4:
            payout_id = self.payout_table.item(row, 0).text()
            action = self.payout_table.item(row, 4).text()
            if action == "Delete":
                self.delete_payout(payout_id)
            return
        group_id = self.payout_table.item(row, 1).text()
        user_id = self.payout_table.item(row, 2).text()
        self.payout_group_id.setCurrentIndex(
            self.payout_group_id.findData(group_id) if group_id else -1
        )
        self.payout_user_id.setCurrentIndex(
            self.payout_user_id.findData(user_id) if user_id else -1
        )
        self.payout_amount.setText(self.payout_table.item(row, 3).text())

    def update_payout(self):
        group_id = self.payout_group_id.currentData()
        user_id = self.payout_user_id.currentData()
        amount = self.payout_amount.text()
        selected_row = self.payout_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Select a payout to update")
            return
        payout_id = self.payout_table.item(selected_row, 0).text()
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
            if not all([group_id, user_id]):
                raise ValueError("Group and user are required")
            response = requests.put(
                f"http://127.0.0.1:8000/payouts/{payout_id}",
                json={"group_id": str(group_id), "user_id": str(user_id), "amount": amount},
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            self.db.update_payout(payout_id, group_id, user_id, amount)
            QMessageBox.information(self, "Success", "Payout updated")
            self.load_payouts()
            self.payout_amount.clear()
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Invalid input: {str(e)}")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to update payout: {str(e)}")

    def delete_payout(self, payout_id):
        reply = QMessageBox.question(self, "Confirm", "Delete this payout?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return
        try:
            response = requests.delete(
                f"http://127.0.0.1:8000/payouts/{payout_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            self.db.delete_payout(payout_id)
            QMessageBox.information(self, "Success", "Payout deleted")
            self.load_payouts()
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to delete payout: {str(e)}")

    def load_users(self):
        session = self.db.Session()
        try:
            users = session.query(User).all()
            self.user_table.setRowCount(len(users))
            for row, user in enumerate(users):
                self.user_table.setItem(row, 0, QTableWidgetItem(str(user.id)))
                self.user_table.setItem(row, 1, QTableWidgetItem(user.username))
                self.user_table.setItem(row, 2, QTableWidgetItem(user.role))
                delete_btn = QTableWidgetItem("Delete")
                delete_btn.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.user_table.setItem(row, 3, delete_btn)
        finally:
            session.close()

    def load_groups(self):
        session = self.db.Session()
        try:
            groups = session.query(Group).all()
            self.group_table.setRowCount(len(groups))
            for row, group in enumerate(groups):
                self.group_table.setItem(row, 0, QTableWidgetItem(str(group.id)))
                self.group_table.setItem(row, 1, QTableWidgetItem(group.name))
                self.group_table.setItem(row, 2, QTableWidgetItem(str(group.balance)))
                delete_btn = QTableWidgetItem("Delete")
                delete_btn.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.group_table.setItem(row, 3, delete_btn)
        finally:
            session.close()

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
                delete_btn = QTableWidgetItem("Delete")
                delete_btn.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.contribution_table.setItem(row, 4, delete_btn)
            self.populate_user_dropdown(self.contribution_user_id)
            self.populate_group_dropdown(self.contribution_group_id)
        finally:
            session.close()

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
                delete_btn = QTableWidgetItem("Delete")
                delete_btn.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.loan_table.setItem(row, 5, delete_btn)
            self.populate_user_dropdown(self.loan_user_id)
            self.populate_group_dropdown(self.loan_group_id)
        finally:
            session.close()

    def load_payouts(self):
        session = self.db.Session()
        try:
            payouts = session.query(Payout).all()
            self.payout_table.setRowCount(len(payouts))
            for row, payout in enumerate(payouts):
                self.payout_table.setItem(row, 0, QTableWidgetItem(str(payout.id)))
                self.payout_table.setItem(row, 1, QTableWidgetItem(str(payout.group_id)))
                self.payout_table.setItem(row, 2, QTableWidgetItem(str(payout.user_id)))
                self.payout_table.setItem(row, 3, QTableWidgetItem(str(payout.amount)))
                delete_btn = QTableWidgetItem("Delete")
                delete_btn.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.payout_table.setItem(row, 4, delete_btn)
            self.populate_user_dropdown(self.payout_user_id)
            self.populate_group_dropdown(self.payout_group_id)
        finally:
            session.close()

    def load_summary(self):
        summary = self.db.get_summary()
        text = "=== Group Balances ===\n"
        for group in summary['groups']:
            text += f"Group: {group['name']} (ID: {group['id'][:8]}...)\n"
            text += f"Balance: {group['balance']:.2f}\n\n"
        text += "=== Loan Statuses ===\n"
        for loan in summary['loans']:
            text += f"Loan ID: {loan['id'][:8]}...\n"
            text += f"User ID: {loan['user_id'][:8]}...\n"
            text += f"Amount: {loan['amount']:.2f}\n"
            text += f"Status: {loan['status']}\n\n"
        self.summary_text.setText(text)

    def perform_sync(self):
        entries = self.db.get_pending_sync_entries()
        if not entries:
            self.sync_text.setText("No pending sync entries.")
            return
        try:
            response = requests.post(
                "http://127.0.0.1:8000/sync",
                json=entries,
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            results = response.json().get("results", [])
            text = "Sync Results:\n"
            for result in results:
                text += f"Entry ID: {result['id'][:8]}... - {result['status']}"
                if result['status'] == "success":
                    self.db.clear_sync_entry(result['id'])
                else:
                    text += f" (Error: {result.get('error', 'Unknown')})"
                text += "\n"
            self.sync_text.setText(text)
            self.load_users()
            self.load_groups()
            self.load_contributions()
            self.load_loans()
            self.load_payouts()
            self.load_summary()
        except requests.RequestException as e:
            self.sync_text.setText(f"Sync failed: {str(e)}")
