use rusqlite::{Connection, Result, params};

pub fn init_database() -> Result<Connection> {
    // ... (keep the existing init_database code)
}

// Struct to represent a User
#[derive(Debug)]
pub struct User {
    pub id: i32,
    pub username: String,
    pub password: String, // In a real app, hash this!
    pub role: String,
    pub group_id: Option<i32>,
}

// CRUD operations for users
pub fn create_user(
    conn: &Connection,
    username: &str,
    password: &str,
    role: &str,
    group_id: Option<i32>,
) -> Result<i32> {
    conn.execute(
        "INSERT INTO users (username, password, role, group_id) VALUES (?1, ?2, ?3, ?4)",
        params![username, password, role, group_id],
    )?;
    Ok(conn.last_insert_rowid() as i32)
}

pub fn get_user_by_id(conn: &Connection, id: i32) -> Result<Option<User>> {
    let mut stmt = conn.prepare("SELECT id, username, password, role, group_id FROM users WHERE id = ?1")?;
    let mut rows = stmt.query_map([id], |row| {
        Ok(User {
            id: row.get(0)?,
            username: row.get(1)?,
            password: row.get(2)?,
            role: row.get(3)?,
            group_id: row.get(4)?,
        })
    })?;

    Ok(rows.next().transpose()?)
}

pub fn update_user(
    conn: &Connection,
    id: i32,
    username: &str,
    password: &str,
    role: &str,
    group_id: Option<i32>,
) -> Result<()> {
    conn.execute(
        "UPDATE users SET username = ?1, password = ?2, role = ?3, group_id = ?4 WHERE id = ?5",
        params![username, password, role, group_id, id],
    )?;
    Ok(())
}

pub fn delete_user(conn: &Connection, id: i32) -> Result<()> {
    conn.execute("DELETE FROM users WHERE id = ?1", [id])?;
    Ok(())
}
