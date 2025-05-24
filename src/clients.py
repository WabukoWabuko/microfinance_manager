import hashlib
import re

class ClientManager:
    def __init__(self):
        from src.database import Database
        self.db = Database()
        print("ClientManager initialized")

    def add_client(self, name, email, phone, role):
        try:
            if not name or not email or not phone or not role:
                return False, "All fields are required"
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return False, "Invalid email format"
            if not re.match(r"\+?\d{10,15}", phone):
                return False, "Invalid phone number format"
            if role not in ["client", "admin"]:
                return False, "Invalid role"
            
            # Generate default password (e.g., "password123")
            password = "password123"
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            query = """
                INSERT INTO Users (name, email, phone, password_hash, role)
                VALUES (?, ?, ?, ?, ?)
            """
            self.db.execute(query, (name, email, phone, password_hash, role))
            return True, "Client added successfully"
        except Exception as e:
            print(f"Error adding client: {e}")
            return False, str(e)

    def close(self):
        try:
            self.db.close()
            print("ClientManager closed")
        except Exception as e:
            print(f"Error closing ClientManager: {e}")
