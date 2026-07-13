import sqlite3

DB_NAME = "database.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS representatives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            status INTEGER DEFAULT 1
        )
    """)

    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM representatives")

    if cursor.fetchone()[0] == 0:

        cursor.executemany("""
            INSERT INTO representatives(name, phone, status)
            VALUES (?, ?, ?)
        """, [
            ("Ahmet", "905551111111", 1),
            ("Mehmet", "905552222222", 1),
            ("Ayşe", "905553333333", 0),
        ])

        conn.commit()

    conn.close()


def get_representatives():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM representatives
        ORDER BY id
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]