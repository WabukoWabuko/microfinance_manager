from datetime import datetime, timedelta
from src.database import Database
import uuid

class LoanManager:
    def __init__(self):
        try:
            self.db = Database()
        except Exception as e:
            print(f"Error in LoanManager.__init__: {e}")
            raise

    def apply_loan(self, user_id, amount, interest_rate, purpose):
        try:
            loan_id = str(uuid.uuid4())
            date_issued = datetime.now().isoformat()
            due_date = (datetime.now() + timedelta(days=365)).isoformat()
            query = """
                INSERT INTO loans (id, user_id, group_id, amount, interest_rate, date_issued, due_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
            """
            self.db.execute(query, (loan_id, str(user_id), None, amount, interest_rate, date_issued, due_date))
            return True, "Loan application submitted"
        except Exception as e:
            print(f"Error in apply_loan: {e}")
            return False, str(e)

    def approve_loan(self, loan_id):
        try:
            query = "UPDATE loans SET status = 'approved' WHERE id = ?"
            self.db.execute(query, (str(loan_id),))
            return True, "Loan approved"
        except Exception as e:
            print(f"Error in approve_loan: {e}")
            return False, str(e)

    def get_loans(self, user_id):
        try:
            query = "SELECT id, amount, status, date_issued FROM loans WHERE user_id = ?"
            return self.db.execute_fetch_all(query, (str(user_id),))
        except Exception as e:
            print(f"Error in get_loans: {e}")
            raise

    def calculate_monthly_payment(self, amount, interest_rate, term_months):
        try:
            monthly_rate = interest_rate / 100 / 12
            monthly_payment = amount * (monthly_rate * (1 + monthly_rate)
                                        ** term_months) / ((1 + monthly_rate) ** term_months - 1)
            return round(monthly_payment, 2)
        except Exception as e:
            print(f"Error in calculate_monthly_payment: {e}")
            raise

    def close(self):
        try:
            self.db.close()
        except Exception as e:
            print(f"Error in close: {e}")
            raise
