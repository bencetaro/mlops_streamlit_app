import sqlite3
from datetime import datetime

DB_PATH = "db/predictions.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    # Single prediction table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS single_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            size REAL,
            n_rooms INTEGER,
            quality INTEGER,
            predicted_price REAL
        )
    """)
    # Batch prediction table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS batch_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            rows_count INTEGER,
            avg_price REAL
        )
    """)
    conn.commit()
    conn.close()

def log_single(size, rooms, quality, price):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO single_predictions 
        (timestamp, size, n_rooms, quality, predicted_price)
        VALUES (?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        size,
        rooms,
        quality,
        price
    ))
    conn.commit()
    conn.close()

def log_batch(rows_count, avg_price):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO batch_predictions 
        (timestamp, rows_count, avg_price)
        VALUES (?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        rows_count,
        avg_price
    ))
    conn.commit()
    conn.close()
