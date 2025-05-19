from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QMessageBox
import requests

class SyncWindow(QDialog):
    def __init__(self, token):
        super().__init__()
        self.setWindowTitle("Sync Data")
        self.setFixedSize(300, 150)
        self.token = token

        # Layout and widgets
        layout = QVBoxLayout()

        sync_button = QPushButton("Sync Now")
        sync_button.clicked.connect(self.perform_sync)
        layout.addWidget(sync_button)

        self.setLayout(layout)

    def perform_sync(self):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/sync",
                json={},
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            QMessageBox.information(self, "Success", "Sync initiated (placeholder)")
            self.accept()
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Sync failed: {str(e)}")
