import sqlite3
from datetime import datetime
import os

DATABASE = 'reviews.db'

def get_db_connection():
    """Create database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows column access by name
    return conn

def init_db():
    """Initialize database and create reviews table"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rating INTEGER NOT NULL,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database initialized!")

def add_review(name, rating, text):
    """Add new review to database"""
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO reviews (name, rating, text) VALUES (?, ?, ?)',
        (name, rating, text)
    )
    review_id = cursor.lastrowid
    conn.commit()
    
    # Get the just created review
    review = conn.execute(
        'SELECT * FROM reviews WHERE id = ?',
        (review_id,)
    ).fetchone()
    conn.close()
    
    return dict(review)

def get_reviews():
    """Get all reviews from database (sorted by newest first)"""
    conn = get_db_connection()
    reviews = conn.execute(
        'SELECT * FROM reviews ORDER BY created_at DESC'
    ).fetchall()
    conn.close()
    
    # Convert to list of dictionaries
    return [dict(review) for review in reviews]
