# Microfinance/Savings Group Manager Design

## Core Entities
- **User**: Represents an individual user (e.g., group member or admin).
  - Fields: ID, username, password (hashed), role (admin/member), group_id.
- **Group**: A savings group with multiple members.
  - Fields: ID, name, description, created_date, balance.
- **Contribution**: A member’s payment to the group.
  - Fields: ID, user_id, group_id, amount, date, status (pending/synced).
- **Loan**: A loan taken by a member from the group.
  - Fields: ID, user_id, group_id, amount, interest_rate, date_issued, due_date, status (active/repaid).
- **Payout**: A distribution of funds to members.
  - Fields: ID, group_id, user_id, amount, date, status (pending/synced).

  ## Database Schema

### Local Storage (SQLite)
- **users** table:
  - id: INTEGER PRIMARY KEY
  - username: TEXT NOT NULL UNIQUE
  - password: TEXT NOT NULL (hashed)
  - role: TEXT NOT NULL (admin/member)
  - group_id: INTEGER (foreign key to groups)
- **groups** table:
  - id: INTEGER PRIMARY KEY
  - name: TEXT NOT NULL
  - description: TEXT
  - created_date: TEXT NOT NULL (ISO 8601 format)
  - balance: REAL NOT NULL
- **contributions** table:
  - id: INTEGER PRIMARY KEY
  - user_id: INTEGER (foreign key to users)
  - group_id: INTEGER (foreign key to groups)
  - amount: REAL NOT NULL
  - date: TEXT NOT NULL
  - status: TEXT NOT NULL (pending/synced)
- **loans** table:
  - id: INTEGER PRIMARY KEY
  - user_id: INTEGER (foreign key to users)
  - group_id: INTEGER (foreign key to groups)
  - amount: REAL NOT NULL
  - interest_rate: REAL NOT NULL
  - date_issued: TEXT NOT NULL
  - due_date: TEXT NOT NULL
  - status: TEXT NOT NULL (active/repaid)
- **payouts** table:
  - id: INTEGER PRIMARY KEY
  - group_id: INTEGER (foreign key to groups)
  - user_id: INTEGER (foreign key to users)
  - amount: REAL NOT NULL
  - date: TEXT NOT NULL
  - status: TEXT NOT NULL (pending/synced)

### Cloud Storage (PostgreSQL)
- Same schema as SQLite, but use SERIAL for auto-incrementing IDs instead of INTEGER PRIMARY KEY.
- Add a **sync_log** table for tracking sync operations:
  - id: SERIAL PRIMARY KEY
  - operation: TEXT NOT NULL (insert/update/delete)
  - entity: TEXT NOT NULL (user/group/contribution/loan/payout)
  - entity_id: INTEGER NOT NULL
  - timestamp: TIMESTAMP NOT NULL

## Offline-Online Sync Mechanism
- **Offline Mode**:
  - Store all transactions (contributions, loans, payouts) in local SQLite database.
  - Mark transactions as "pending" in the `status` field.
  - Maintain a queue of operations (insert/update/delete) in a local `sync_queue` table:
    - id: INTEGER PRIMARY KEY
    - operation: TEXT (insert/update/delete)

## Security Measures
- **User Authentication**: Use JWT (JSON Web Tokens) for secure login.
- **Data Encryption**:
  - Hash passwords using bcrypt before storing.
  - Encrypt sensitive data (e.g., transaction amounts) in SQLite using `rusqlite` encryption extensions.
  - Use HTTPS for API communication.
- **Secure APIs**:
  - Validate all inputs to prevent SQL injection.
  - Require JWT authentication for all endpoints except login.
