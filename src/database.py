import sqlite3
import bcrypt
import uuid

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
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    group_id TEXT
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS groups (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_date TIMESTAMP NOT NULL,
                    balance REAL NOT NULL
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS contributions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    group_id TEXT NOT NULL,
                    amount REAL NOT NULL,
                    date TIMESTAMP NOT NULL,
                    status TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (group_id) REFERENCES groups(id)
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS loans (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    group_id TEXT NOT NULL,
                    amount REAL NOT NULL,
                    interest_rate REAL NOT NULL,
                    date_issued TIMESTAMP NOT NULL,
                    due_date TIMESTAMP NOT NULL,
                    status TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (group_id) REFERENCES groups(id)
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS payouts (
                    id TEXT PRIMARY KEY,
                    group_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    amount REAL NOT NULL,
                    date TIMESTAMP NOT NULL,
                    status TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (group_id) REFERENCES groups(id)
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS sync_queue (
                    id TEXT PRIMARY KEY,
                    operation TEXT NOT NULL,
                    entity TEXT NOT NULL,
                    entity_id TEXT NOT NULL,
                    data TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL
                )
            ''')
            self.conn.commit()
            self.seed_admin_user()
        except Exception as e:
            print(f"Error in create_tables: {e}")
            raise

    def seed_admin_user(self):
        try:
            user_id = str(uuid.uuid4())
            username = "john@example.com"
            password = "password"
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self.cursor.execute('''
                INSERT OR IGNORE INTO users (id, username, password, role, group_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, username, hashed, "client", None))
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
