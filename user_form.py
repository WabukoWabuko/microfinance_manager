from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
import requests
from local_db import LocalDatabase

class UserForm(QDialog):
    def __init__(self, token):
        super().__init__()
        self.setWindowTitle("Manage Users")
        self.setFixedSize(600, 400)
        self.token = token
        self.db = LocalDatabase()

        # Layout and widgets
        layout = QVBoxLayout()

        # Form for creating users
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)

        self.role_input = QLineEdit()
        self.role_input.setPlaceholderText("Role (e.g., admin, member)")
        layout.addWidget(QLabel("Role:"))
        layout.addWidget(self.role_input)

        create_button = QPushButton("Create User")
        create_button.clicked.connect(self.create_user)
        layout.addWidget(create_button)

        # Table for displaying users
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(3)
        self.user_table.setHorizontalHeaderLabels(["ID", "Username", "Role"])
        self.user_table.setColumnWidth(0, 200)
        self.user_table.setColumnWidth(1, 150)
        self.user_table.setColumnWidth(2, 100)
        layout.addWidget(QLabel("Users:"))
        layout.addWidget(self.user_table)

        refresh_button = QPushButton("Refresh Users")
        refresh_button.clicked.connect(self.load_users)
        layout.addWidget(refresh_button)

        self.setLayout(layout)
        self.load_users()

    def create_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_input.text()

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
            QMessageBox.information(self, "Success", "User created successfully")
            self.load_users()
            self.username_input.clear()
            self.password_input.clear()
            self.role_input.clear()
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to create user: {str(e)}")

    def load_users(self):
        session = self.db.Session()
        try:
            users = session.query(self.db.User).all()
            self.user_table.setRowCount(len(users))
            for row, user in enumerate(users):
                self.user_table.setItem(row, 0, QTableWidgetItem(str(user.id)))
                self.user_table.setItem(row, 1, QTableWidgetItem(user.username))
                self.user_table.setItem(row, 2, QTableWidgetItem(user.role))
        finally:
            session.close()
