import csv
from src.database import Database


class ExportManager:
    def __init__(self):
        try:
            self.db = Database()
            print("ExportManager initialized")
        except Exception as e:
            print(f"Error in ExportManager.__init__: {e}")
            raise

    def export_data(self, user_id, format_type):
        try:
            data = self.db.fetchall(
                "SELECT * FROM Transactions WHERE loan_id IN (SELECT id FROM Loans WHERE user_id = ?)", (user_id,))
            if format_type == "CSV":
                with open(f"export_{user_id}.csv", "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(
                        ["ID", "Loan ID", "Amount", "Type", "Created At"])
                    writer.writerows(data)
                return True, "Exported to CSV"
            elif format_type == "PDF":
                # Placeholder for PDF export (requires reportlab or similar)
                return False, "PDF export not implemented"
            return False, "Unsupported format"
        except Exception as e:
            print(f"Error in export_data: {e}")
            return False, str(e)

    def close(self):
        try:
            self.db.close()
            print("ExportManager closed")
        except Exception as e:
            print(f"Error in close: {e}")
