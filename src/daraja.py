import requests
import base64
import time
from datetime import datetime
from decouple import config

class DarajaAPI:
   def __init__(self):
       self.base_url = "https://sandbox.safaricom.co.ke"
       self.api_key = config("MPESA_API_KEY")
       self.api_secret = config("MPESA_API_SECRET")
       self.shortcode = config("SHORTCODE")
       self.passkey = config("PASSKEY")
       self.callback_url = config("CALLBACK_URL")
       self.access_token = None
       self.token_expiry = 0

   def get_access_token(self):
       """Obtain OAuth access token."""
       if self.access_token and time.time() < self.token_expiry:
           return self.access_token
       auth = base64.b64encode(f"{self.api_key}:{self.api_secret}".encode()).decode()
       headers = {"Authorization": f"Basic {auth}"}
       url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
       try:
           response = requests.get(url, headers=headers, timeout=10)
           response.raise_for_status()
           data = response.json()
           self.access_token = data["access_token"]
           self.token_expiry = time.time() + int(data["expires_in"]) - 60
           return self.access_token
       except requests.RequestException as e:
           return None, f"Failed to get access token: {str(e)}"

   def initiate_stk_push(self, phone_number, amount, transaction_id):
       """Initiate STK Push for a transaction."""
       access_token = self.get_access_token()
       if not access_token:
           return False, "Authentication failed"
       timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
       password = base64.b64encode(f"{self.shortcode}{self.passkey}{timestamp}".encode()).decode()
       payload = {
           "BusinessShortCode": self.shortcode,
           "Password": password,
           "Timestamp": timestamp,
           "TransactionType": "CustomerPayBillOnline",
           "Amount": int(amount),
           "PartyA": phone_number,
           "PartyB": self.shortcode,
           "PhoneNumber": phone_number,
           "CallBackURL": self.callback_url,
           "AccountReference": f"TRX{transaction_id}",
           "TransactionDesc": "Microfinance Payment"
       }
       headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
       url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
       try:
           response = requests.post(url, json=payload, headers=headers, timeout=10)
           response.raise_for_status()
           data = response.json()
           if data.get("ResponseCode") == "0":
               return True, data["CheckoutRequestID"]
           return False, data.get("errorMessage", "STK Push failed")
       except requests.RequestException as e:
           return False, f"STK Push error: {str(e)}"

   def query_transaction_status(self, checkout_request_id):
       """Query the status of an STK Push transaction."""
       access_token = self.get_access_token()
       if not access_token:
           return False, "Authentication failed"
       timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
       password = base64.b64encode(f"{self.shortcode}{self.passkey}{timestamp}".encode()).decode()
       payload = {
           "BusinessShortCode": self.shortcode,
           "Password": password,
           "Timestamp": timestamp,
           "CheckoutRequestID": checkout_request_id
       }
       headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
       url = f"{self.base_url}/mpesa/stkpushquery/v1/query"
       try:
           response = requests.post(url, json=payload, headers=headers, timeout=10)
           response.raise_for_status()
           data = response.json()
           if data.get("ResultCode") == "0":
               return True, "Transaction completed"
           return False, data.get("ResultDesc", "Transaction failed")
       except requests.RequestException as e:
           return False, f"Status query error: {str(e)}"
