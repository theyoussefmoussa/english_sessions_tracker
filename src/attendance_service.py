"""Database functions for the Streamlit app.

Unlike the CLI versions, these functions never call input() or print().
They take plain arguments, return data, and raise exceptions, so the
Streamlit UI decides how to display results and errors.
"""
import psycopg

from database.connection import get_connection


class DatabaseConnectionError(Exception):
    """Raised when get_connection() cannot connect to the database."""


def _connect():
    conn = get_connection()
    if conn is None:
        raise DatabaseConnectionError("Unable to connect to the database.")
    return conn


def get_active_students():
    """Return [(username, full_name, grade), ...] for active students."""
    conn = _connect()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT username, full_name, grade::text
                    FROM students
                    WHERE is_active = TRUE
                    ORDER BY full_name;
                """)
                return cur.fetchall()
    finally:
        conn.close()


def get_attendance_status(username, date):
    """Return 'Present' / 'Absent' if a record exists, otherwise None."""
    conn = _connect()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT status FROM attendance
                    WHERE username = %s AND date = %s;
                """, (username, date))
                row = cur.fetchone()
                return row[0] if row else None
    finally:
        conn.close()


def insert_attendance(username, date, status):
    """Insert a new record. Raises psycopg.errors.UniqueViolation if it exists."""
    conn = _connect()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO attendance (username, date, status)
                    VALUES (%s, %s, %s);
                """, (username, date, status))
    finally:
        conn.close()


def update_attendance(username, date, status):
    """Overwrite the status of an existing record."""
    conn = _connect()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE attendance
                    SET status = %s
                    WHERE username = %s AND date = %s;
                """, (status, username, date))
    finally:
        conn.close()


def get_all_attendance():
    """Return (column_names, rows) for every attendance record."""
    conn = _connect()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM attendance
                    ORDER BY date DESC, attendance_id DESC;
                """)
                columns = [col.name for col in cur.description]
                return columns, cur.fetchall()
    finally:
        conn.close()

def get_attendance_for_date(date):
    """Return {username: status} for every record on the given date."""
    conn = _connect()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT username, status FROM attendance
                    WHERE date = %s;
                """, (date,))
                return dict(cur.fetchall())
    finally:
        conn.close()


def save_bulk_attendance(date, statuses):
    """Insert or update attendance for many students in ONE transaction.

    statuses: {username: 'Present' | 'Absent'}
    Existing records for that date are updated, new ones are inserted.
    Returns the number of rows saved. If any row fails, nothing is saved.
    """
    rows = [(username, date, status) for username, status in statuses.items()]
    conn = _connect()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.executemany("""
                    INSERT INTO attendance (username, date, status)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (username, date)
                    DO UPDATE SET status = EXCLUDED.status;
                """, rows)
        return len(rows)
    finally:
        conn.close()