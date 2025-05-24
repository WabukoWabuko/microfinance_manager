import bcrypt
from src.database import Database

class Auth:
    def __init__(self):
        try:
            self.db = Database()
        except Exception as e:
            print(f"Error in Auth.__init__: {e}")
            raise

    def login(self, email, password):
        try:
            result = self.db.execute_fetch_one(
                "SELECT id, name, email, password_hash, phone, role FROM Users WHERE email = ?",
                (email,)
            )
            if result:
                stored_hash = result[3].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                    return True, {
                        "id": result[0],
                        "name": result[1],
                        "email": result[2],
                        "phone": result[4],
                        "role": result[5]
                    }
                return False, "Invalid password"
            return False, "User not found"
        except Exception as e:
            print(f"Error in login: {e}")
            return False, str(e)

    def close(self):
        try:
            self.db.close()
        except Exception as e:
            print(f"Error in close: {e}")
            raise
