# database.py
import sqlite3
import pandas as pd
from datetime import datetime

DATABASE_NAME = "resumes.db"

def get_connection():
    """Returns a new connection to the SQLite database."""
    return sqlite3.connect(DATABASE_NAME, check_same_thread=False)

def initialize_db():
    """Creates the resumes table if it does not exist."""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            resume_link TEXT,
            resume_text TEXT,
            location TEXT,
            similarity_score REAL,
            timestamp TEXT
        );
    ''')
    conn.commit()
    conn.close()

def update_resumes(student_data):
    """Bulk inserts or replaces resume records from the provided DataFrame."""
    conn = get_connection()
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    records = []

    required_columns = ['First name', 'Email id', 'Resume link', 'Location']
    missing_columns = [col for col in required_columns if col not in student_data.columns]
    if missing_columns:
        raise ValueError(f"Missing columns in CSV: {', '.join(missing_columns)}")

    for _, row in student_data.iterrows():
        name = row['First name']
        email = row['Email id']
        resume_link = row['Resume link']
        location = row['Location']
        resume_text = row.get('ResumeText', "")
        records.append((name, email, resume_link, resume_text, location, 0.0, timestamp))

    c.executemany('''
        INSERT OR REPLACE INTO resumes (name, email, resume_link, resume_text, location, similarity_score, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', records)
    conn.commit()
    conn.close()

def fetch_resumes(location_filter=None):
    """Fetches resumes from the database, optionally filtering by location."""
    conn = get_connection()
    if location_filter:
        query = "SELECT name, email, resume_text, resume_link, location FROM resumes WHERE location LIKE ?"
        df = pd.read_sql(query, conn, params=(f'%{location_filter}%',))
    else:
        df = pd.read_sql("SELECT name, email, resume_text, resume_link, location FROM resumes", conn)
    conn.close()
    return df
