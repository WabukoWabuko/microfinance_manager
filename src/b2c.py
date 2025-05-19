from src.daraja import DarajaAPI

class B2CManager:
    def __init__(self):
        try:
            self.daraja_api = DarajaAPI()
            print("B2CManager initialized")
        except Exception as e:
            print(f"Error in B2CManager.__init__: {e}")
            raise

    def withdraw(self, user_id, amount, phone):
        try:
            response = self.daraja_api.b2c_payment(amount, phone)
            return True, "Withdrawal successful"
        except Exception as e:
            print(f"Error in withdraw: {e}")
            return False, str(e)

    def close(self):
        try:
            print("B2CManager closed")
        except Exception as e:
            print(f"Error in close: {e}")
