import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(BASE_DIR, "database.db")


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def _column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cursor.fetchall())


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS representatives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            status INTEGER NOT NULL DEFAULT 1,
            sort_order INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    conn.commit()

    # Migration guard: eski tablolarda eksik sütunları ekle.
    if not _column_exists(cursor, "representatives", "created_at"):
        cursor.execute(
            "ALTER TABLE representatives ADD COLUMN created_at TEXT"
        )
        cursor.execute(
            "UPDATE representatives SET created_at = datetime('now') "
            "WHERE created_at IS NULL"
        )
        conn.commit()

    if not _column_exists(cursor, "representatives", "sort_order"):
        cursor.execute(
            "ALTER TABLE representatives ADD COLUMN sort_order INTEGER DEFAULT 0"
        )
        # Mevcut kayıtlara id sırasına göre başlangıç sırası ver.
        cursor.execute("UPDATE representatives SET sort_order = id")
        conn.commit()

    cursor.execute("SELECT COUNT(*) FROM representatives")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO representatives(name, phone, status, sort_order)
            VALUES (?, ?, ?, ?)
        """, [
            ("Ahmet", "905551111111", 1, 1),
            ("Mehmet", "905552222222", 1, 2),
            ("Ayşe", "905553333333", 0, 3),
        ])
        conn.commit()

    conn.close()


def get_representatives():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM representatives ORDER BY sort_order, id")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_representative(rep_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM representatives WHERE id = ?",
        (rep_id,),
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def add_representative(name, phone, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(MAX(sort_order), 0) + 1 FROM representatives")
    next_order = cursor.fetchone()[0]
    cursor.execute("""
        INSERT INTO representatives(name, phone, status, sort_order, created_at)
        VALUES (?, ?, ?, ?, datetime('now'))
    """, (name, phone, int(status), next_order))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def update_representative(rep_id, name, phone, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE representatives
        SET name = ?, phone = ?, status = ?
        WHERE id = ?
    """, (name, phone, int(status), rep_id))
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated


def toggle_status(rep_id):
    """Temsilcinin online/offline durumunu tersine çevirir. Yeni durumu döner."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT status FROM representatives WHERE id = ?",
        (rep_id,),
    )
    row = cursor.fetchone()
    if row is None:
        conn.close()
        return None
    new_status = 0 if row["status"] == 1 else 1
    cursor.execute(
        "UPDATE representatives SET status = ? WHERE id = ?",
        (new_status, rep_id),
    )
    conn.commit()
    conn.close()
    return new_status


def reorder_representatives(ordered_ids):
    """Verilen id sırasına göre sort_order alanlarını günceller."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executemany(
        "UPDATE representatives SET sort_order = ? WHERE id = ?",
        [(index, rep_id) for index, rep_id in enumerate(ordered_ids)],
    )
    conn.commit()
    conn.close()


def delete_representative(rep_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM representatives WHERE id = ?",
        (rep_id,),
    )
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return deleted
