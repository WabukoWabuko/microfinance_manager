import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        try:
            self.conn = sqlite3.connect("microfinance.db")
            self.cursor = self.conn.cursor()
            self.init_db()
            print("Database initialized")
        except Exception as e:
            print(f"Error in Database.__init__: {e}")
            raise

    def init_db(self):
        try:
            self.cursor.executescript("""
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE,
                    password TEXT,
                    name TEXT,
                    role TEXT
                );
                CREATE TABLE IF NOT EXISTS Loans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    amount REAL,
                    interest_rate REAL,
                    purpose TEXT,
                    status TEXT,
                    created_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES Users(id)
                );
                CREATE TABLE IF NOT EXISTS Transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    loan_id INTEGER,
                    amount REAL,
                    type TEXT,
                    created_at TIMESTAMP,
                    FOREIGN KEY (loan_id) REFERENCES Loans(id)
                );
                CREATE TABLE IF NOT EXISTS Settings (
                    id INTEGER PRIMARY KEY,
                    theme TEXT,
                    last_sync_timestamp TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS AuditLogs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT,
                    details TEXT,
                    timestamp TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS Notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    message TEXT,
                    created_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES Users(id)
                );
                CREATE TABLE IF NOT EXISTS Profiles (
                    user_id INTEGER PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    phone TEXT,
                    FOREIGN KEY (user_id) REFERENCES Users(id)
                );
                CREATE TABLE IF NOT EXISTS TwoFactor (
                    user_id INTEGER PRIMARY KEY,
                    secret TEXT,
                    enabled BOOLEAN,
                    FOREIGN KEY (user_id) REFERENCES Users(id)
                );
                CREATE TABLE IF NOT EXISTS OfflineCache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT,
                    data TEXT,
                    created_at TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS Widgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    type TEXT,
                    config TEXT,
                    FOREIGN KEY (user_id) REFERENCES Users(id)
                );
                CREATE TABLE IF NOT EXISTS Repayments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    loan_id INTEGER,
                    due_date TIMESTAMP,
                    amount REAL,
                    status TEXT,
                    FOREIGN KEY (loan_id) REFERENCES Loans(id)
                );
            """)
            self.conn.commit()
            # Insert default user
            self.cursor.execute("SELECT COUNT(*) FROM Users")
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute("INSERT INTO Users (email, password, name, role) VALUES (?, ?, ?, ?)",
                                    ("john@example.com", "password", "John Doe", "client"))
                self.conn.commit()
            print("Database schema initialized")
        except Exception as e:
            print(f"Error in init_db: {e}")
            raise

    def execute(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error in execute: {e}")
            return False

    def fetchall(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error in fetchall: {e}")
            return []

    def close(self):
        try:
            self.conn.close()
            print("Database closed")
        except Exception as e:
            print(f"Error in close: {e}")
