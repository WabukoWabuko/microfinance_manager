from src.database import Database


class PasswordResetManager:
    def __init__(self):
        try:
            self.db = Database()
            print("PasswordResetManager initialized")
        except Exception as e:
            print(f"Error in PasswordResetManager.__init__: {e}")
            raise

    def initiate_reset(self, email):
        try:
            user = self.db.fetchall(
                "SELECT id FROM Users WHERE email = ?", (email,))
            if user:
                # Placeholder for sending reset email
                return True, "Reset link sent to your email"
            return False, "Email not found"
        except Exception as e:
            print(f"Error in initiate_reset: {e}")
            return False, str(e)

    def close(self):
        try:
            self.db.close()
            print("PasswordResetManager closed")
        except Exception as e:
            print(f"Error in close: {e}")
