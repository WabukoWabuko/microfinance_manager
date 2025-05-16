use rusqlite::{params, Connection, Result};
use std::time::{SystemTime, UNIX_EPOCH};

// Structs for entities
#[derive(Debug)]
struct User {
    id: i32,
    username: String,
    password: String, // In production, hash this!
    role: String,
    group_id: Option<i32>,
}

#[derive(Debug)]
struct Group {
    id: i32,
    name: String,
    description: Option<String>,
    created_date: String,
    balance: f64,
}

#[derive(Debug)]
struct Contribution {
    id: i32,
    user_id: i32,
    group_id: i32,
    amount: f64,
    date: String,
    status: String,
}

#[derive(Debug)]
struct Loan {
    id: i32,
    user_id: i32,
    group_id: i32,
    amount: f64,
    interest_rate: f64,
    date_issued: String,
    due_date: String,
    status: String,
}

#[derive(Debug)]
struct Payout {
    id: i32,
    group_id: i32,
    user_id: i32,
    amount: f64,
    date: String,
    status: String,
}

#[derive(Debug)]
struct SyncQueue {
    id: i32,
    operation: String,
    entity: String,
    entity_id: i32,
    data: String,
    created_at: String,
}

// Database setup and CRUD operations
struct Database {
    conn: Connection,
}

impl Database {
    // Initialize database and create tables
    fn new() -> Result<Self> {
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
    fn create_user(&self, username: &str, password: &str, role: &str, group_id: Option<i32>) -> Result<i32> {
        self.conn.execute(
            "INSERT INTO users (username, password, role, group_id) VALUES (?1, ?2, ?3, ?4)",
            params![username, password, role, group_id],
        )?;
        Ok(self.conn.last_insert_rowid() as i32)
    }

    fn get_user(&self, id: i32) -> Result<Option<User>> {
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
    fn create_group(&self, name: &str, description: Option<&str>, balance: f64) -> Result<i32> {
        let created_date = Self::get_timestamp();
        self.conn.execute(
            "INSERT INTO groups (name, description, created_date, balance) VALUES (?1, ?2, ?3, ?4)",
            params![name, description, created_date, balance],
        )?;
        Ok(self.conn.last_insert_rowid() as i32)
    }

    fn get_group(&self, id: i32) -> Result<Option<Group>> {
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
    fn create_contribution(&self, user_id: i32, group_id: i32, amount: f64) -> Result<i32> {
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

    fn get_contribution(&self, id: i32) -> Result<Option<Contribution>> {
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

    // Loan CRUD (simplified, similar pattern)
    fn create_loan(&self, user_id: i32, group_id: i32, amount: f64, interest_rate: f64, due_date: &str) -> Result<i32> {
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

    // Payout CRUD (simplified)
    fn create_payout(&self, group_id: i32, user_id: i32, amount: f64) -> Result<i32> {
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
}

fn main() -> Result<()> {
    // Initialize database
    let db = Database::new()?;
    println!("Database initialized with all tables.");

    // Create a user
    let user_id = db.create_user("alice", "password123", "admin", None)?;
    println!("Created user with ID: {}", user_id);

    // Create a group
    let group_id = db.create_group("Savings Group 1", Some("First savings group"), 1000.0)?;
    println!("Created group with ID: {}", group_id);

    // Create a contribution
    let contribution_id = db.create_contribution(user_id, group_id, 50.0)?;
    println!("Created contribution with ID: {}", contribution_id);

    // Create a loan
    let loan_id = db.create_loan(user_id, group_id, 200.0, 5.0, "2025-12-01T00:00:00Z")?;
    println!("Created loan with ID: {}", loan_id);

    // Create a payout
    let payout_id = db.create_payout(group_id, user_id, 100.0)?;
    println!("Created payout with ID: {}", payout_id);

    // Read and display a user
    if let Some(user) = db.get_user(user_id)? {
        println!("Fetched user: {:?}", user);
    }

    // Read and display a group
    if let Some(group) = db.get_group(group_id)? {
        println!("Fetched group: {:?}", group);
    }

    // Read and display a contribution
    if let Some(contribution) = db.get_contribution(contribution_id)? {
        println!("Fetched contribution: {:?}", contribution);
    }

    Ok(())
}
