import psycopg

from database.connection import get_connection
from utils.validators import validate_full_name, validate_grade, validate_student_username


def is_unique_username(username):
    conn = get_connection()

    if conn is None:
        raise ConnectionError("Unable to connect to the database.")

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT EXISTS (
                        SELECT 1
                        FROM students
                        WHERE username = %s
                    );
                    """,
                    (username,),
                )

                username_exists = cur.fetchone()[0]

        return not username_exists

    finally:
        conn.close()


def get_students():
    conn = get_connection()

    if conn is None:
        print("Unable to connect to the database. Please try again.")
        return None

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT student_id, full_name, username, grade
                    FROM students
                    ORDER BY student_id;
                    """
                )
                students = cur.fetchall()

        return students

    except psycopg.Error as error:
        print(f"Failed to retrieve students: {error}")
        return None

    finally:
        conn.close()

def add_student():
    full_name = validate_full_name()
    grade = validate_grade()

    while True:
        username = validate_student_username()

        try:
            if is_unique_username(username):
                break

            print("Username is already taken. Please choose a different username.")

        except ConnectionError as error:
            print(error)
            return

    conn = get_connection()

    if conn is None:
        print("Unable to connect to the database. Please try again.")
        return

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO students (full_name, grade, username)
                    VALUES (%s, %s, %s)
                    """,
                    (full_name, grade, username),
                )

        print(f"Student {full_name} added successfully!")
        print(f"Student username: {username}")

    except psycopg.Error as error:
        print(f"Failed to add student: {error}")

    finally:
        conn.close()
