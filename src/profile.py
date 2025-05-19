from src.database import Database

class ProfileManager:
    def __init__(self):
        try:
            self.db = Database()
            print("ProfileManager initialized")
        except Exception as e:
            print(f"Error in ProfileManager.__init__: {e}")
            raise

    def update_profile(self, user_id, name, email):
        try:
            self.db.execute("INSERT OR REPLACE INTO Profiles (user_id, name, email, phone) VALUES (?, ?, ?, ?)",
                            (user_id, name, email, ""))
            return True, "Profile updated"
        except Exception as e:
            print(f"Error in update_profile: {e}")
            return False, str(e)

    def close(self):
        try:
            self.db.close()
            print("ProfileManager closed")
        except Exception as e:
            print(f"Error in close: {e}")
