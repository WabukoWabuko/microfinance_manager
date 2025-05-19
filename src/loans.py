from datetime import datetime
from database import Database

class LoanManager:
   def __init__(self):
       self.db = Database()

   def apply_loan(self, user_id, amount, interest_rate, purpose):
       """Apply for a new loan."""
       applied_date = datetime.now().isoformat()
       query = """
           INSERT INTO Loans (user_id, amount, interest_rate, status, applied_date)
           VALUES (?, ?, ?, 'pending', ?)
       """
       self.db.execute(query, (user_id, amount, interest_rate, applied_date))
       return True, "Loan application submitted"

   def approve_loan(self, loan_id):
       """Approve a loan."""
       approved_date = datetime.now().isoformat()
       query = "UPDATE Loans SET status = 'approved', approved_date = ? WHERE id = ?"
       self.db.execute(query, (approved_date, loan_id))
       return True, "Loan approved"

   def get_loans(self, user_id):
       """Retrieve all loans for a user."""
       query = "SELECT id, amount, interest_rate, status, applied_date, approved_date FROM Loans WHERE user_id = ?"
       return self.db.fetch_all(query, (user_id,))

   def calculate_monthly_payment(self, amount, interest_rate, term_months):
       """Calculate monthly repayment for a loan."""
       monthly_rate = interest_rate / 100 / 12
       monthly_payment = amount * (monthly_rate * (1 + monthly_rate) ** term_months) / ((1 + monthly_rate) ** term_months - 1)
       return round(monthly_payment, 2)

   def close(self):
       """Close the database connection."""
       self.db.close()
