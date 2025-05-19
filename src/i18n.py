class I18nManager:
    def __init__(self):
        try:
            self.current_lang = "en"
            self.translations = {
                "en": {
                    "Enter your registered email": "Enter your registered email",
                    "Enter your password": "Enter your password",
                    "Select your role": "Select your role",
                    "Click to log in": "Click to log in",
                    "Reset your password": "Reset your password",
                    "View your dashboard": "View your dashboard",
                    "Apply for a new loan": "Apply for a new loan",
                    "View transaction history": "View transaction history",
                    "View loan analytics": "View loan analytics",
                    "View repayment schedule": "View repayment schedule",
                    "Edit your profile": "Edit your profile",
                    "Sync transactions with MPesa": "Sync transactions with MPesa",
                    "Calculate monthly payment": "Calculate monthly payment",
                    "Submit loan application": "Submit loan application",
                    "Return to previous page": "Return to previous page",
                    "Withdraw funds via MPesa": "Withdraw funds via MPesa",
                    "Export data to CSV/PDF": "Export data to CSV/PDF",
                    "View notifications": "View notifications",
                    "Save profile changes": "Save profile changes",
                    "Setup two-factor authentication": "Setup two-factor authentication",
                    "Welcome, {name}!": "Welcome, {name}!",
                    "Error": "Error",
                    "Invalid role": "Invalid role",
                    "Login failed: {error}": "Login failed: {error}",
                    "Loan": "Loan",
                    "Loan submission failed: {error}": "Loan submission failed: {error}",
                    "Calculation failed: {error}": "Calculation failed: {error}",
                    "Sync": "Sync",
                    "Sync failed: {error}": "Sync failed: {error}",
                    "Withdrawal": "Withdrawal",
                    "Withdrawal failed: {error}": "Withdrawal failed: {error}",
                    "Export": "Export",
                    "Export failed: {error}": "Export failed: {error}",
                    "Notifications failed: {error}": "Notifications failed: {error}",
                    "Profile": "Profile",
                    "Profile update failed: {error}": "Profile update failed: {error}",
                    "Two-Factor": "Two-Factor",
                    "Two-factor setup failed: {error}": "Two-factor setup failed: {error}",
                    "Password Reset": "Password Reset",
                    "Password reset failed: {error}": "Password reset failed: {error}",
                    "Monthly Payment: {payment}": "Monthly Payment: {payment}",
                    "Dashboard update failed: {error}": "Dashboard update failed: {error}",
                    "Theme application failed: {error}": "Theme application failed: {error}",
                    "Theme toggle failed: {error}": "Theme toggle failed: {error}",
                    "Navigation failed: {error}": "Navigation failed: {error}",
                    "Ready": "Ready"
                },
                "sw": {
                    "Enter your registered email": "Ingiza barua pepe yako ya usajili",
                    "Enter your password": "Ingiza nenosiri lako",
                    "Select your role": "Chagua jukumu lako",
                    "Click to log in": "Bonyeza kuingia",
                    "Reset your password": "Weka upya nenosiri lako",
                    "View your dashboard": "Angalia dashibodi yako",
                    "Apply for a new loan": "Omba mkopo mpya",
                    "View transaction history": "Angalia historia ya miamala",
                    "View loan analytics": "Angalia uchanganuzi wa mkopo",
                    "View repayment schedule": "Angalia ratiba ya ulipaji",
                    "Edit your profile": "Hariri wasifu wako",
                    "Sync transactions with MPesa": "Sawazisha miamala na MPesa",
                    "Calculate monthly payment": "Hesabu malipo ya kila mwezi",
                    "Submit loan application": "Wasilisha ombi la mkopo",
                    "Return to previous page": "Rudi kwenye ukurasa uliopita",
                    "Withdraw funds via MPesa": "Toa pesa kupitia MPesa",
                    "Export data to CSV/PDF": "Hamisha data kwa CSV/PDF",
                    "View notifications": "Angalia arifa",
                    "Save profile changes": "Hifadhi mabadiliko ya wasifu",
                    "Setup two-factor authentication": "Sanidi uthibitishaji wa hatua mbili",
                    "Welcome, {name}!": "Karibu, {name}!",
                    "Error": "Hitilafu",
                    "Invalid role": "Jukumu batili",
                    "Login failed: {error}": "Kuingia kumeshindwa: {error}",
                    "Loan": "Mkopo",
                    "Loan submission failed: {error}": "Uwasilishaji wa mkopo umeshindwa: {error}",
                    "Calculation failed: {error}": "Hesabu imeshindwa: {error}",
                    "Sync": "Sawazisha",
                    "Sync failed: {error}": "Usawazishaji umeshindwa: {error}",
                    "Withdrawal": "Utoaji",
                    "Withdrawal failed: {error}": "Utoaji umeshindwa: {error}",
                    "Export": "Hamisha",
                    "Export failed: {error}": "Uhamishaji umeshindwa: {error}",
                    "Notifications failed: {error}": "Arifa zimeshindwa: {error}",
                    "Profile": "Wasifu",
                    "Profile update failed: {error}": "Usasishaji wa wasifu umeshindwa: {error}",
                    "Two-Factor": "Uthibitishaji wa Hatua Mbili",
                    "Two-factor setup failed: {error}": "Usanidi wa uthibitishaji wa hatua mbili umeshindwa: {error}",
                    "Password Reset": "Weka Upya Nenosiri",
                    "Password reset failed: {error}": "Kuweka upya nenosiri kumeshindwa: {error}",
                    "Monthly Payment: {payment}": "Malipo ya Kila Mwezi: {payment}",
                    "Dashboard update failed: {error}": "Usasishaji wa dashibodi umeshindwa: {error}",
                    "Theme application failed: {error}": "Utekelezaji wa mandhari umeshindwa: {error}",
                    "Theme toggle failed: {error}": "Kugeuza mandhari kumeshindwa: {error}",
                    "Navigation failed: {error}": "Urambazaji umeshindwa: {error}",
                    "Ready": "Tayari"
                }
            }
            print("I18nManager initialized")
        except Exception as e:
            print(f"Error in I18nManager.__init__: {e}")
            raise

    def set_language(self, lang):
        try:
            if lang in self.translations:
                self.current_lang = lang
                print(f"Language set to {lang}")
            else:
                print(f"Language {lang} not supported")
        except Exception as e:
            print(f"Error in set_language: {e}")
            raise

    def translate(self, text):
        try:
            return self.translations[self.current_lang].get(text, text)
        except Exception as e:
            print(f"Error in translate: {e}")
            return text

    def close(self):
        try:
            print("I18nManager closed")
        except Exception as e:
            print(f"Error in close: {e}")
