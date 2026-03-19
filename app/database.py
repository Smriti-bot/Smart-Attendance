import sqlite3


def init_db():
    conn = sqlite3.connect("data/attendance.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    """)

    conn.commit()
    conn.close()


def create_default_admin():
    conn = sqlite3.connect("data/attendance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM admin WHERE username = ?", ("admin",))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO admin (username, password) VALUES (?, ?)",
            ("admin", "admin123")
        )

    conn.commit()
    conn.close()


def insert_attendance(name, date, time):
    conn = sqlite3.connect("data/attendance.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO attendance (name, date, time)
        VALUES (?, ?, ?)
    """, (name, date, time))

    conn.commit()
    conn.close()


def check_duplicate(name, date):
    conn = sqlite3.connect("data/attendance.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM attendance
        WHERE name = ? AND date = ?
    """, (name, date))

    result = cursor.fetchone()

    conn.close()
    return result