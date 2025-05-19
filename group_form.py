from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
import requests
from local_db import LocalDatabase

class GroupForm(QDialog):
    def __init__(self, token):
        super().__init__()
        self.setWindowTitle("Manage Groups")
        self.setFixedSize(600, 350)
        self.token = token
        self.db = LocalDatabase()

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

        # Table for displaying groups
        self.group_table = QTableWidget()
        self.group_table.setColumnCount(3)
        self.group_table.setHorizontalHeaderLabels(["ID", "Name", "Balance"])
        self.group_table.setColumnWidth(0, 200)
        self.group_table.setColumnWidth(1, 150)
        self.group_table.setColumnWidth(2, 100)
        layout.addWidget(QLabel("Groups:"))
        layout.addWidget(self.group_table)

        refresh_button = QPushButton("Refresh Groups")
        refresh_button.clicked.connect(self.load_groups)
        layout.addWidget(refresh_button)

        self.setLayout(layout)
        self.load_groups()

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
            self.load_groups()
            self.name_input.clear()
            self.description_input.clear()
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to create group: {str(e)}")

    def load_groups(self):
        session = self.db.Session()
        try:
            groups = session.query(self.db.Group).all()
            self.group_table.setRowCount(len(groups))
            for row, group in enumerate(groups):
                self.group_table.setItem(row, 0, QTableWidgetItem(str(group.id)))
                self.group_table.setItem(row, 1, QTableWidgetItem(group.name))
                self.group_table.setItem(row, 2, QTableWidgetItem(str(group.balance)))
        finally:
            session.close()
