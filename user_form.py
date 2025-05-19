from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import requests

class UserForm(QDialog):
    def __init__(self, token):
        super().__init__()
        self.setWindowTitle("Manage Users")
        self.setFixedSize(300, 250)
        self.token = token

        # Layout and widgets
        layout = QVBoxLayout()

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

        self.setLayout(layout)

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
            self.accept()
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to create user: {str(e)}")
