#[allow(dead_code)] // Suppress warnings until fields are used in UI/backend
#[derive(Debug)]
pub struct User {
    pub id: i32,
    pub username: String,
    pub password: String, // In production, hash this!
    pub role: String,
    pub group_id: Option<i32>,
}

#[allow(dead_code)]
#[derive(Debug)]
pub struct Group {
    pub id: i32,
    pub name: String,
    pub description: Option<String>,
    pub created_date: String,
    pub balance: f64,
}

#[allow(dead_code)]
#[derive(Debug)]
pub struct Contribution {
    pub id: i32,
    pub user_id: i32,
    pub group_id: i32,
    pub amount: f64,
    pub date: String,
    pub status: String,
}

#[derive(Debug)]
pub struct Loan {
    pub id: i32,
    pub user_id: i32,
    pub group_id: i32,
    pub amount: f64,
    pub interest_rate: f64,
    pub date_issued: String,
    pub due_date: String,
    pub status: String,
}

#[derive(Debug)]
pub struct Payout {
    pub id: i32,
    pub group_id: i32,
    pub user_id: i32,
    pub amount: f64,
    pub date: String,
    pub status: String,
}

#[derive(Debug)]
pub struct SyncQueue {
    pub id: i32,
    pub operation: String,
    pub entity: String,
    pub entity_id: i32,
    pub data: String,
    pub created_at: String,
}
