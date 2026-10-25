import psycopg

from utils.validators import validate_full_name, validate_grade
from database.connection import get_connection


def add_student():
    full_name = validate_full_name()
    grade = validate_grade()

    conn = get_connection()

    # Check if the connection was successful 
    if conn is None:
        print("Unable to connect to the database. Please try again.")
        return

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO students (full_name, grade) VALUES (%s, %s)",
                    (full_name, grade)
                )

        print(f"Student {full_name} added successfully!")

    except psycopg.Error as error:
        print(f"Failed to add student: {error}")

    finally:
        conn.close()