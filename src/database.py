import sqlite3
import bcrypt

class Database:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('microfinance.db')
            self.cursor = self.conn.cursor()
            self.create_tables()
        except Exception as e:
            print(f"Error in Database.__init__: {e}")
            raise

    def create_tables(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    phone TEXT,
                    role TEXT NOT NULL,
                    two_factor_enabled BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Loans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    amount REAL NOT NULL,
                    interest_rate REAL NOT NULL,
                    term INTEGER NOT NULL,
                    purpose TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES Users(id)
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    loan_id INTEGER,
                    amount REAL NOT NULL,
                    type TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (loan_id) REFERENCES Loans(id)
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Settings (
                    id INTEGER PRIMARY KEY,
                    theme TEXT DEFAULT 'light',
                    last_sync_timestamp TIMESTAMP
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS AuditLog (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    details TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES Users(id)
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    message TEXT NOT NULL,
                    status TEXT DEFAULT 'unread',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES Users(id)
                )
            ''')
            self.conn.commit()
            self.seed_admin_user()
        except Exception as e:
            print(f"Error in create_tables: {e}")
            raise

    def seed_admin_user(self):
        try:
            email = "john@example.com"
            password = "password"
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self.cursor.execute('''
                INSERT OR IGNORE INTO Users (name, email, password_hash, phone, role)
                VALUES (?, ?, ?, ?, ?)
            ''', ("John Doe", email, hashed.decode('utf-8'), "+254123456789", "client"))
            self.conn.commit()
        except Exception as e:
            print(f"Error in seed_admin_user: {e}")
            raise

    def execute(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            print(f"Error in execute: {e}")
            raise

    def execute_fetch_one(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            print(f"Error fetching one: {e}")
            raise

    def execute_fetch_all(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching all: {e}")
            raise

    def close(self):
        try:
            self.conn.close()
        except Exception as e:
            print(f"Error in close: {e}")
            raise
