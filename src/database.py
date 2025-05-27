import sqlite3
import bcrypt
import uuid
import logging

class Database:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, filename='debug.log', filemode='a',
                           format='%(asctime)s - %(levelname)s - %(message)s')
        logging.debug("Initializing Database")
        try:
            self.conn = sqlite3.connect('microfinance.db')
            self.conn.row_factory = sqlite3.Row  # Enable dictionary-like row access
            self.cursor = self.conn.cursor()
            self.create_tables()
            logging.debug("Database initialized")
        except Exception as e:
            logging.error(f"Error in Database.__init__: {e}")
            raise

    def create_tables(self):
        logging.debug("Creating tables")
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    group_id TEXT,
                    two_factor_enabled BOOLEAN DEFAULT 0
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
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id TEXT PRIMARY KEY,
                    loan_id TEXT NOT NULL,
                    amount REAL NOT NULL,
                    type TEXT NOT NULL,
                    date TIMESTAMP NOT NULL,
                    status TEXT NOT NULL,
                    FOREIGN KEY (loan_id) REFERENCES loans(id)
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS AuditLog (
                    id TEXT PRIMARY KEY,
                    user_id TEXT,
                    action TEXT NOT NULL,
                    details TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            self.conn.commit()
            self.seed_admin_user()
            logging.debug("Tables created and seeded")
        except Exception as e:
            logging.error(f"Error in create_tables: {e}")
            raise

    def seed_admin_user(self):
        logging.debug("Seeding users")
        try:
            # Client user
            user_id = str(uuid.uuid4())
            username = "john@example.com"
            password = "password"
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self.cursor.execute('''
                INSERT OR IGNORE INTO users (id, username, password, role, group_id, two_factor_enabled)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, username, hashed, "Client", None, 0))
            # Admin user
            admin_id = str(uuid.uuid4())
            admin_username = "admin@example.com"
            self.cursor.execute('''
                INSERT OR IGNORE INTO users (id, username, password, role, group_id, two_factor_enabled)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (admin_id, admin_username, hashed, "Admin", None, 0))
            self.conn.commit()
            logging.debug("Users seeded: john@example.com (Client), admin@example.com (Admin)")
        except Exception as e:
            logging.error(f"Error in seed_admin_user: {e}")
            raise

    def get_user_by_email(self, email):
        logging.debug(f"Querying user by email: {email}")
        try:
            self.cursor.execute('SELECT * FROM users WHERE username = ?', (email,))
            user = self.cursor.fetchone()
            if user:
                logging.debug("User found")
                return {
                    'user_id': user['id'],
                    'email': user['username'],
                    'password': user['password'],
                    'role': user['role']
                }
            logging.debug("User not found")
            return None
        except Exception as e:
            logging.error(f"Error in get_user_by_email: {e}")
            return None

    def execute(self, query, params=()):
        logging.debug(f"Executing query: {query}")
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            logging.error(f"Error in execute: {e}")
            raise

    def execute_fetch_one(self, query, params=()):
        logging.debug(f"Fetching one: {query}")
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            logging.error(f"Error fetching one: {e}")
            raise

    def execute_fetch_all(self, query, params=()):
        logging.debug(f"Fetching all: {query}")
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            logging.error(f"Error fetching all: {e}")
            raise

    def close(self):
        logging.debug("Closing database connection")
        try:
            self.conn.close()
        except Exception as e:
            logging.error(f"Error in close: {e}")
            raise
