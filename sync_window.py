from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QMessageBox, QTextEdit
import requests
from local_db import LocalDatabase

class SyncWindow(QDialog):
    def __init__(self, token):
        super().__init__()
        self.setWindowTitle("Sync Data")
        self.setFixedSize(400, 300)
        self.token = token
        self.db = LocalDatabase()

        # Layout and widgets
        layout = QVBoxLayout()

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        sync_button = QPushButton("Sync Now")
        sync_button.clicked.connect(self.perform_sync)
        layout.addWidget(sync_button)

        self.setLayout(layout)

    def perform_sync(self):
        # Get pending sync entries
        try:
            entries = self.db.get_pending_sync_entries()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch sync entries: {str(e)}")
            return

        if not entries:
            self.result_text.setText("No pending sync entries.")
            return

        # Send to backend
        try:
            response = requests.post(
                "http://127.0.0.1:8000/sync",
                json=entries,
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            results = response.json().get("results", [])

            # Process results
            output = []
            for result in results:
                sync_id = result["id"]
                status = result["status"]
                error = result.get("error", "")
                output.append(f"Sync ID: {sync_id}, Status: {status}")
                if error:
                    output.append(f"Error: {error}")
                if status == "success":
                    try:
                        self.db.clear_sync_entry(sync_id)
                    except Exception as e:
                        output.append(f"Failed to clear sync entry {sync_id}: {str(e)}")

            self.result_text.setText("\n".join(output))
            QMessageBox.information(self, "Success", "Sync completed")
        except requests.RequestException as e:
            self.result_text.setText(f"Sync failed: {str(e)}")
            QMessageBox.critical(self, "Error", f"Sync failed: {str(e)}")
