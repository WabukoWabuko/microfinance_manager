import sqlite3
from pathlib import Path

class Database:
   def __init__(self):
       self.db_path = Path("db/microfinance.db")
       self.db_path.parent.mkdir(exist_ok=True)
       self.conn = sqlite3.connect(self.db_path)
       self.cursor = self.conn.cursor()
       self.create_tables()

   def create_tables(self):
       """Initialize SQLite tables for users, loans, transactions, and settings."""
       self.cursor.execute("""
           CREATE TABLE IF NOT EXISTS Users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               role TEXT NOT NULL CHECK(role IN ('client', 'admin', 'officer')),
               name TEXT NOT NULL,
               email TEXT UNIQUE NOT NULL,
               phone TEXT UNIQUE NOT NULL,
               password_hash TEXT NOT NULL
           )
       """)
       self.cursor.execute("""
           CREATE TABLE IF NOT EXISTS Loans (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER NOT NULL,
               amount REAL NOT NULL,
               interest_rate REAL NOT NULL,
               status TEXT NOT NULL CHECK(status IN ('pending', 'approved', 'repaid')),
               applied_date TEXT NOT NULL,
               approved_date TEXT,
               FOREIGN KEY (user_id) REFERENCES Users(id)
           )
       """)
       self.cursor.execute("""
           CREATE TABLE IF NOT EXISTS Transactions (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               loan_id INTEGER,
               amount REAL NOT NULL,
               type TEXT NOT NULL CHECK(type IN ('deposit', 'withdrawal')),
               date TEXT NOT NULL,
               sync_status TEXT NOT NULL CHECK(sync_status IN ('pending', 'synced')),
               FOREIGN KEY (loan_id) REFERENCES Loans(id)
           )
       """)
       self.cursor.execute("""
           CREATE TABLE IF NOT EXISTS Settings (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               theme TEXT NOT NULL CHECK(theme IN ('dark', 'light')),
               last_sync_timestamp TEXT
           )
       """)
       self.conn.commit()

   def execute(self, query, params=()):
       """Execute a query with optional parameters."""
       self.cursor.execute(query, params)
       self.conn.commit()

   def fetch_all(self, query, params=()):
       """Fetch all results from a query."""
       self.cursor.execute(query, params)
       return self.cursor.fetchall()

   def fetch_one(self, query, params=()):
       """Fetch one result from a query."""
       self.cursor.execute(query, params)
       return self.cursor.fetchone()

   def close(self):
       """Close the database connection."""
       self.conn.close()
