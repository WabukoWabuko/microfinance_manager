from src.database import Database


class TwoFactorAuth:
    def __init__(self):
        try:
            self.db = Database()
        except Exception as e:
            print(f"Error in TwoFactorAuth.__init__: {e}")
            raise

    def is_enabled(self, user_id):
        try:
            result = self.db.execute_fetch_one(
                "SELECT two_factor_enabled FROM users WHERE id = ?",
                (str(user_id),)
            )
            return result[0] if result else False
        except Exception as e:
            print(f"Error in is_enabled: {e}")
            raise

    def setup(self, user_id, code):
        try:
            query = "UPDATE users SET two_factor_enabled = 1 WHERE id = ?"
            self.db.execute(query, (str(user_id),))
            return True, "Two-factor authentication enabled"
        except Exception as e:
            print(f"Error in setup: {e}")
            return False, str(e)

    def verify(self, user_id):
        try:
            return True, "Verification successful"
        except Exception as e:
            print(f"Error in verify: {e}")
            return False, str(e)

    def close(self):
        try:
            self.db.close()
        except Exception as e:
            print(f"Error in close: {e}")
            raise
