import sys
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import requests
from gui import MainWindow

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(300, 150)
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
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)
        
        self.setLayout(layout)
    
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password")
            return
        try:
            response = requests.post(
                "http://127.0.0.1:8000/login",
                json={"username": username, "password": password}
            )
            response.raise_for_status()
            self.token = response.json().get("token")
            self.accept()
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Login failed: {str(e)}")

def main():
    app = QApplication(sys.argv)
    login_dialog = LoginDialog()
    if login_dialog.exec():
        window = MainWindow(login_dialog.token)
        window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()
