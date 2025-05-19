from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import requests

class GroupForm(QDialog):
    def __init__(self, token):
        super().__init__()
        self.setWindowTitle("Manage Groups")
        self.setFixedSize(300, 200)
        self.token = token

        # Layout and widgets
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Group Name")
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)

        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Description (optional)")
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_input)

        create_button = QPushButton("Create Group")
        create_button.clicked.connect(self.create_group)
        layout.addWidget(create_button)

        self.setLayout(layout)

    def create_group(self):
        name = self.name_input.text()
        description = self.description_input.text() or None

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
            QMessageBox.information(self, "Success", "Group created successfully")
            self.accept()
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to create group: {str(e)}")
