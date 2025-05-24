import bcrypt
from src.database import Database


class Auth:
    def __init__(self):
        try:
            self.db = Database()
        except Exception as e:
            print(f"Error in Auth.__init__: {e}")
            raise

    def login(self, username, password):
        try:
            result = self.db.execute_fetch_one(
                "SELECT id, username, password, role FROM users WHERE username = ?",
                (username,)
            )
            if result:
                stored_hash = result[2]
                if isinstance(stored_hash, str):
                    stored_hash = stored_hash.encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                    return True, {
                        "id": result[0],
                        "username": result[1],
                        "role": result[3]
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
