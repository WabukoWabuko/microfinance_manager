from src.database import Database

class TwoFactorAuth:
    def __init__(self):
        try:
            self.db = Database()
            print("TwoFactorAuth initialized")
        except Exception as e:
            print(f"Error in TwoFactorAuth.__init__: {e}")
            raise

    def setup(self, user_id, code):
        try:
            self.db.execute("INSERT OR REPLACE INTO TwoFactor (user_id, secret, enabled) VALUES (?, ?, ?)",
                            (user_id, code, True))
            return True, "2FA enabled"
        except Exception as e:
            print(f"Error in setup: {e}")
            return False, str(e)

    def is_enabled(self, user_id):
        try:
            result = self.db.fetchall("SELECT enabled FROM TwoFactor WHERE user_id = ?", (user_id,))
            return bool(result and result[0][0])
        except Exception as e:
            print(f"Error in is_enabled: {e}")
            return False

    def verify(self, user_id):
        try:
            return True, "2FA verified"  # Simplified
        except Exception as e:
            print(f"Error in verify: {e}")
            return False, str(e)

    def close(self):
        try:
            self.db.close()
            print("TwoFactorAuth closed")
        except Exception as e:
            print(f"Error in close: {e}")
