from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import requests
from gui import MainWindow

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Microfinance Manager - Login")
        self.setFixedSize(300, 200)

        # Layout and widgets
        widget = QWidget()
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

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.token = None

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return

        try:
            response = requests.post(
                "http://127.0.0.1:8000/login",
                json={"username": username, "password": password}
            )
            response.raise_for_status()
            self.token = response.json().get("token")
            self.open_main_window()
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Login failed: {str(e)}")

    def open_main_window(self):
        self.main_window = MainWindow(self.token)
        self.main_window.show()
        self.close()
