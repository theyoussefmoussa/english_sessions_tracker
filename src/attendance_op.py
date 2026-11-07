import psycopg

from database.connection import get_connection
from utils.validators import validate_attendance_date, validate_attendance_status, validate_student_username


def mark_attendance():
    username = validate_student_username()
    date = validate_attendance_date()
    status = validate_attendance_status()

    conn = get_connection()

    if conn is None:
        print("Unable to connect to the database. Please try again.")
        return

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO attendance (username, date, status)
                    VALUES (%s, %s, %s)
                """, (username, date, status))

                print(
                    f"Attendance for {username} on {date} "
                    f"has been recorded as {status}."
                )
    except psycopg.errors.UniqueViolation:
        print(f"Attendance for {username} on {date} has already been recorded.")

    except psycopg.Error as e:
        print(f"Database error: {e}")

    finally:
        conn.close()


def view_attendance():
    conn = get_connection()

    if conn is None:
        print("Unable to connect to database.")
        return

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM attendance;
                """)

                records = cur.fetchall()

                if not records:
                    print("No attendance records found.")
                    return

                for record in records:
                    print(record)

    except psycopg.Error as e:
        print(f"Database error: {e}")

    finally:
        conn.close()