mod models;
mod database;

use database::Database;
use rusqlite::Result;

fn main() -> Result<()> {
    // Initialize database
    let db = Database::new()?;
    println!("Database initialized with all tables.");

    // Check if user exists, create if not
    let user_id = match db.get_user_by_username("alice")? {
        Some(user) => {
            println!("User 'alice' already exists with ID: {}", user.id);
            user.id
        }
        None => {
            let id = db.create_user("alice", "password123", "admin", None)?;
            println!("Created user with ID: {}", id);
            id
        }
    };

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

    // Read and display a loan
    if let Some(loan) = db.get_loan(loan_id)? {
        println!("Fetched loan: {:?}", loan);
    }

    // Read and display a payout
    if let Some(payout) = db.get_payout(payout_id)? {
        println!("Fetched payout: {:?}", payout);
    }

    // Read and display a sync queue entry (using contribution_id as it creates a sync entry)
    if let Some(sync_entry) = db.get_sync_queue(contribution_id)? {
        println!("Fetched sync queue entry: {:?}", sync_entry);
    }

    Ok(())
}
