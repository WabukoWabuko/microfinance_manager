import sqlite3
import hashlib
import os
from datetime import datetime

class Database:
    def __init__(self):
        try:
            db_path = os.path.expanduser("~/Desktop/all/microfinance_manager/microfinance.db")
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            self.create_tables()
            print("Database initialized")
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise

    def create_tables(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Loans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    amount REAL NOT NULL,
                    interest_rate REAL NOT NULL,
                    purpose TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES Users(id)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    loan_id INTEGER,
                    amount REAL NOT NULL,
                    type TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (loan_id) REFERENCES Loans(id)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Settings (
                    id INTEGER PRIMARY KEY,
                    theme TEXT NOT NULL,
                    last_sync_timestamp TIMESTAMP
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES Users(id)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS AuditLog (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    details TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES Users(id)
                )
            """)
            self.conn.commit()
            print("Database schema initialized")
        except Exception as e:
            print(f"Error creating tables: {e}")
            raise

    def execute(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            print(f"Error executing query: {e}")
            raise

    def fetch_one(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error fetching one: {e}")
            raise

    def fetch_all(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Error fetching all: {e}")
            raise

    def close(self):
        try:
            self.conn.close()
            print("Database connection closed")
        except Exception as e:
            print(f"Error closing database: {e}")
