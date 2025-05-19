from src.auth import Auth
from src.loans import LoanManager
from src.transactions import TransactionManager


def run_tests():
    # Test authentication
    auth = Auth()
    # Check if user already exists
    email = "john@example.com"
    query = "SELECT id FROM Users WHERE email = ?"
    existing_user = auth.db.fetch_one(query, (email,))
    if not existing_user:
        success, msg = auth.register(
            "John Doe", email, "1234567890", "password", "client")
        print(f"Register: {msg}")
    else:
        print(f"Register: User with email {email} already exists")
    success, user = auth.login(email, "password")
    print(f"Login: {user if success else msg}")
    user_id = user["id"] if success else None

    # Test loan management
    if user_id:
        loan_manager = LoanManager()
        success, msg = loan_manager.apply_loan(user_id, 10000, 5.0, "Business")
        print(f"Apply Loan: {msg}")
        loans = loan_manager.get_loans(user_id)
        print(f"Loans: {loans}")
        payment = loan_manager.calculate_monthly_payment(10000, 5.0, 12)
        print(f"Monthly Payment: {payment}")

    # Test transactions
    if loans:
        loan_id = loans[0][0]
        transaction_manager = TransactionManager()
        success, msg = transaction_manager.record_transaction(
            loan_id, 1000, "deposit")
        print(f"Record Transaction: {msg}")
        transactions = transaction_manager.get_transactions(loan_id)
        print(f"Transactions: {transactions}")

    # Clean up
    auth.close()
    if user_id:
        loan_manager.close()
        transaction_manager.close()


if __name__ == "__main__":
    run_tests()
