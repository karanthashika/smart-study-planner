import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "studyplanner.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():

    conn = get_db_connection()

    conn.executescript("""

    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        study_hours REAL DEFAULT 2,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        difficulty INTEGER NOT NULL,
        preparation INTEGER NOT NULL,
        FOREIGN KEY (user_id)
            REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        completed INTEGER DEFAULT 0,
        FOREIGN KEY (subject_id)
            REFERENCES subjects(id)
    );

    CREATE TABLE IF NOT EXISTS exams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        subject_id INTEGER NOT NULL,
        exam_date TEXT NOT NULL,
        FOREIGN KEY (user_id)
            REFERENCES users(id),
        FOREIGN KEY (subject_id)
            REFERENCES subjects(id)
    );

    CREATE TABLE IF NOT EXISTS study_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        subject_id INTEGER NOT NULL,
        topic_id INTEGER,
        session_date TEXT NOT NULL,
        duration_minutes INTEGER NOT NULL,
        status TEXT DEFAULT 'planned',
        FOREIGN KEY (user_id)
            REFERENCES users(id),
        FOREIGN KEY (subject_id)
            REFERENCES subjects(id),
        FOREIGN KEY (topic_id)
            REFERENCES topics(id)
    );

    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        subject_id INTEGER NOT NULL,
        completion_percent INTEGER DEFAULT 0,
        confidence INTEGER DEFAULT 0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id)
            REFERENCES users(id),
        FOREIGN KEY (subject_id)
            REFERENCES subjects(id)
    );

    """)

    # Add study_hours to an existing database if it does not exist yet.
    try:
        conn.execute(
            "ALTER TABLE users ADD COLUMN study_hours REAL DEFAULT 2"
        )
    except sqlite3.OperationalError:
        pass

    conn.execute(
        """
        INSERT OR IGNORE INTO users
        (id, name, email, password, study_hours)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            1,
            "Student",
            "student@example.com",
            "demo",
            2
        )
    )

    conn.commit()
    conn.close()