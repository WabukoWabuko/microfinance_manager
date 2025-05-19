import hashlib
import sqlite3
from datetime import datetime
from database import Database

class Auth:
   def __init__(self):
       self.db = Database()

   def hash_password(self, password):
       """Hash a password using SHA-256."""
       return hashlib.sha256(password.encode()).hexdigest()

   def register(self, name, email, phone, password, role):
       """Register a new user with hashed password."""
       password_hash = self.hash_password(password)
       query = """
           INSERT INTO Users (name, email, phone, password_hash, role)
           VALUES (?, ?, ?, ?, ?)
       """
       try:
           self.db.execute(query, (name, email, phone, password_hash, role))
           return True, "Registration successful"
       except sqlite3.IntegrityError:
           return False, "Email or phone already exists"

   def login(self, email, password):
       """Authenticate a user."""
       password_hash = self.hash_password(password)
       query = "SELECT id, name, role FROM Users WHERE email = ? AND password_hash = ?"
       user = self.db.fetch_one(query, (email, password_hash))
       if user:
           return True, {"id": user[0], "name": user[1], "role": user[2]}
       return False, "Invalid email or password"

   def close(self):
       """Close the database connection."""
       self.db.close()
