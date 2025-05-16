from src.database.local_db import LocalDatabase

def main():
    db = LocalDatabase()
    print("Database initialized with all tables.")

    # Check if user exists, create if not
    user = db.get_user_by_username("alice")
    if user:
        user_id = user.id
        print(f"User 'alice' already exists with ID: {user_id}")
    else:
        user_id = db.create_user("alice", "password123", "admin")
        print(f"Created user with ID: {user_id}")

    # Create a group
    group_id = db.create_group("Savings Group 1", description="First savings group", balance=1000.0)
    print(f"Created group with ID: {group_id}")

    # Create a contribution
    contribution_id = db.create_contribution(user_id, group_id, 50.0)
    print(f"Created contribution with ID: {contribution_id}")

    # Create a loan
    loan_id = db.create_loan(user_id, group_id, 200.0, 5.0, "2025-12-01T00:00:00")
    print(f"Created loan with ID: {loan_id}")

    # Create a payout
    payout_id = db.create_payout(group_id, user_id, 100.0)
    print(f"Created payout with ID: {payout_id}")

    # Fetch and display data
    user = db.get_user(user_id)
    if user:
        print(f"Fetched user: {user.__dict__}")

    group = db.get_group(group_id)
    if group:
        print(f"Fetched group: {group.__dict__}")

    contribution = db.get_contribution(contribution_id)
    if contribution:
        print(f"Fetched contribution: {contribution.__dict__}")

    loan = db.get_loan(loan_id)
    if loan:
        print(f"Fetched loan: {loan.__dict__}")

    payout = db.get_payout(payout_id)
    if payout:
        print(f"Fetched payout: {payout.__dict__}")

    sync_entry = db.get_sync_queue(contribution_id)
    if sync_entry:
        print(f"Fetched sync queue entry: {sync_entry.__dict__}")

if __name__ == "__main__":
    main()
