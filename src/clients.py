import re
import bcrypt
import uuid
from src.database import Database


class ClientManager:
    def __init__(self):
        try:
            self.db = Database()
        except Exception as e:
            print(f"Error in ClientManager.__init__: {e}")
            raise

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

            user_id = str(uuid.uuid4())
            password = "password123"
            password_hash = bcrypt.hashpw(
                password.encode('utf-8'), bcrypt.gensalt())
            query = """
                INSERT INTO users (id, username, password, role, group_id)
                VALUES (?, ?, ?, ?, ?)
            """
            self.db.execute(query, (user_id, email, password_hash, role, None))
            return True, "Client added successfully"
        except Exception as e:
            print(f"Error in add_client: {e}")
            return False, str(e)

    def close(self):
        try:
            self.db.close()
        except Exception as e:
            print(f"Error in close: {e}")
            raise
