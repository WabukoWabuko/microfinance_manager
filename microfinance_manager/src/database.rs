use rusqlite::{params, Connection, Result};
use std::time::{SystemTime, UNIX_EPOCH};
use crate::models::{User, Group, Contribution, Loan, Payout, SyncQueue};

pub struct Database {
    conn: Connection,
}

impl Database {
    // Initialize database and create tables
    pub fn new() -> Result<Self> {
        let conn = Connection::open("microfinance.db")?;
        
        // Create tables
        conn.execute(
            "CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                group_id INTEGER
            )",
            [],
        )?;

        conn.execute(
            "CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                created_date TEXT NOT NULL,
                balance REAL NOT NULL
            )",
            [],
        )?;

        conn.execute(
            "CREATE TABLE IF NOT EXISTS contributions (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                group_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL
            )",
            [],
        )?;

        conn.execute(
            "CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                group_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                interest_rate REAL NOT NULL,
                date_issued TEXT NOT NULL,
                due_date TEXT NOT NULL,
                status TEXT NOT NULL
            )",
            [],
        )?;

        conn.execute(
            "CREATE TABLE IF NOT EXISTS payouts (
                id INTEGER PRIMARY KEY,
                group_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL
            )",
            [],
        )?;

        conn.execute(
            "CREATE TABLE IF NOT EXISTS sync_queue (
                id INTEGER PRIMARY KEY,
                operation TEXT NOT NULL,
                entity TEXT NOT NULL,
                entity_id INTEGER NOT NULL,
                data TEXT NOT NULL,
                created_at TEXT NOT NULL
            )",
            [],
        )?;

        Ok(Database { conn })
    }

    // Get current timestamp as ISO 8601 string
    fn get_timestamp() -> String {
        let now = SystemTime::now();
        let timestamp = now.duration_since(UNIX_EPOCH).unwrap().as_secs();
        // Simplified ISO 8601 format (in production, use a proper datetime library)
        format!("2025-05-16T{}Z", timestamp)
    }

    // User CRUD
    pub fn create_user(&self, username: &str, password: &str, role: &str, group_id: Option<i32>) -> Result<i32> {
        self.conn.execute(
            "INSERT INTO users (username, password, role, group_id) VALUES (?1, ?2, ?3, ?4)",
            params![username, password, role, group_id],
        )?;
        Ok(self.conn.last_insert_rowid() as i32)
    }

    pub fn get_user(&self, id: i32) -> Result<Option<User>> {
        let mut stmt = self.conn.prepare("SELECT id, username, password, role, group_id FROM users WHERE id = ?1")?;
        let mut rows = stmt.query([id])?;
        if let Some(row) = rows.next()? {
            Ok(Some(User {
                id: row.get(0)?,
                username: row.get(1)?,
                password: row.get(2)?,
                role: row.get(3)?,
                group_id: row.get(4)?,
            }))
        } else {
            Ok(None)
        }
    }

    // Group CRUD
    pub fn create_group(&self, name: &str, description: Option<&str>, balance: f64) -> Result<i32> {
        let created_date = Self::get_timestamp();
        self.conn.execute(
            "INSERT INTO groups (name, description, created_date, balance) VALUES (?1, ?2, ?3, ?4)",
            params![name, description, created_date, balance],
        )?;
        Ok(self.conn.last_insert_rowid() as i32)
    }

    pub fn get_group(&self, id: i32) -> Result<Option<Group>> {
        let mut stmt = self.conn.prepare("SELECT id, name, description, created_date, balance FROM groups WHERE id = ?1")?;
        let mut rows = stmt.query([id])?;
        if let Some(row) = rows.next()? {
            Ok(Some(Group {
                id: row.get(0)?,
                name: row.get(1)?,
                description: row.get(2)?,
                created_date: row.get(3)?,
                balance: row.get(4)?,
            }))
        } else {
            Ok(None)
        }
    }

    // Contribution CRUD
    pub fn create_contribution(&self, user_id: i32, group_id: i32, amount: f64) -> Result<i32> {
        let date = Self::get_timestamp();
        let status = "pending";
        self.conn.execute(
            "INSERT INTO contributions (user_id, group_id, amount, date, status) VALUES (?1, ?2, ?3, ?4, ?5)",
            params![user_id, group_id, amount, date, status],
        )?;
        let id = self.conn.last_insert_rowid() as i32;

        // Add to sync queue
        self.conn.execute(
            "INSERT INTO sync_queue (operation, entity, entity_id, data, created_at) VALUES (?1, ?2, ?3, ?4, ?5)",
            params!["insert", "contribution", id, format!("{{\"user_id\":{},\"group_id\":{},\"amount\":{}}}", user_id, group_id, amount), date],
        )?;
        Ok(id)
    }

    pub fn get_contribution(&self, id: i32) -> Result<Option<Contribution>> {
        let mut stmt = self.conn.prepare("SELECT id, user_id, group_id, amount, date, status FROM contributions WHERE id = ?1")?;
        let mut rows = stmt.query([id])?;
        if let Some(row) = rows.next()? {
            Ok(Some(Contribution {
                id: row.get(0)?,
                user_id: row.get(1)?,
                group_id: row.get(2)?,
                amount: row.get(3)?,
                date: row.get(4)?,
                status: row.get(5)?,
            }))
        } else {
            Ok(None)
        }
    }

    // Loan CRUD
    pub fn create_loan(&self, user_id: i32, group_id: i32, amount: f64, interest_rate: f64, due_date: &str) -> Result<i32> {
        let date_issued = Self::get_timestamp();
        let status = "active";
        self.conn.execute(
            "INSERT INTO loans (user_id, group_id, amount, interest_rate, date_issued, due_date, status) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)",
            params![user_id, group_id, amount, interest_rate, date_issued, due_date, status],
        )?;
        let id = self.conn.last_insert_rowid() as i32;

        // Add to sync queue
        self.conn.execute(
            "INSERT INTO sync_queue (operation, entity, entity_id, data, created_at) VALUES (?1, ?2, ?3, ?4, ?5)",
            params!["insert", "loan", id, format!("{{\"user_id\":{},\"group_id\":{},\"amount\":{}}}", user_id, group_id, amount), date_issued],
        )?;
        Ok(id)
    }

    pub fn get_loan(&self, id: i32) -> Result<Option<Loan>> {
        let mut stmt = self.conn.prepare("SELECT id, user_id, group_id, amount, interest_rate, date_issued, due_date, status FROM loans WHERE id = ?1")?;
        let mut rows = stmt.query([id])?;
        if let Some(row) = rows.next()? {
            Ok(Some(Loan {
                id: row.get(0)?,
                user_id: row.get(1)?,
                group_id: row.get(2)?,
                amount: row.get(3)?,
                interest_rate: row.get(4)?,
                date_issued: row.get(5)?,
                due_date: row.get(6)?,
                status: row.get(7)?,
            }))
        } else {
            Ok(None)
        }
    }

    // Payout CRUD
    pub fn create_payout(&self, group_id: i32, user_id: i32, amount: f64) -> Result<i32> {
        let date = Self::get_timestamp();
        let status = "pending";
        self.conn.execute(
            "INSERT INTO payouts (group_id, user_id, amount, date, status) VALUES (?1, ?2, ?3, ?4, ?5)",
            params![group_id, user_id, amount, date, status],
        )?;
        let id = self.conn.last_insert_rowid() as i32;

        // Add to sync queue
        self.conn.execute(
            "INSERT INTO sync_queue (operation, entity, entity_id, data, created_at) VALUES (?1, ?2, ?3, ?4, ?5)",
            params!["insert", "payout", id, format!("{{\"group_id\":{},\"user_id\":{},\"amount\":{}}}", group_id, user_id, amount), date],
        )?;
        Ok(id)
    }

    pub fn get_payout(&self, id: i32) -> Result<Option<Payout>> {
        let mut stmt = self.conn.prepare("SELECT id, group_id, user_id, amount, date, status FROM payouts WHERE id = ?1")?;
        let mut rows = stmt.query([id])?;
        if let Some(row) = rows.next()? {
            Ok(Some(Payout {
                id: row.get(0)?,
                group_id: row.get(1)?,
                user_id: row.get(2)?,
                amount: row.get(3)?,
                date: row.get(4)?,
                status: row.get(5)?,
            }))
        } else {
            Ok(None)
        }
    }

    // SyncQueue CRUD
    pub fn get_sync_queue(&self, id: i32) -> Result<Option<SyncQueue>> {
        let mut stmt = self.conn.prepare("SELECT id, operation, entity, entity_id, data, created_at FROM sync_queue WHERE id = ?1")?;
        let mut rows = stmt.query([id])?;
        if let Some(row) = rows.next()? {
            Ok(Some(SyncQueue {
                id: row.get(0)?,
                operation: row.get(1)?,
                entity: row.get(2)?,
                entity_id: row.get(3)?,
                data: row.get(4)?,
                created_at: row.get(5)?,
            }))
        } else {
            Ok(None)
        }
    }
}
