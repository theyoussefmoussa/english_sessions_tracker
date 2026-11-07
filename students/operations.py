import psycopg

from utils.validators import (
    is_unique_username,
    validate_full_name,
    validate_grade,
    validate_student_username,
)
from database.connection import get_connection
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


def view_students():
    students = get_students()

    if students is None:
        return

    if students:
        print("List of Students:")

        for student in students:
            print(
                f"ID: {student[0]}, "
                f"Name: {student[1]}, "
                f"Username: {student[2]}, "
                f"Grade: {student[3]}"
            )
    else:
        print("No students found.")


def get_student_by_username(username):
    username = username.strip().lower()
    conn = get_connection()

    if conn is None:
        raise ConnectionError("Unable to connect to the database.")

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT student_id, full_name, grade
                    FROM students
                    WHERE username = %s
                    """,
                    (username,),
                )

                return cur.fetchone()

    finally:
        conn.close()


def view_student_by_username():
    while True:
        username = input("Enter the student's username: ").strip().lower()

        if not username:
            print("Username cannot be empty. Please try again.")
            continue

        try:
            student = get_student_by_username(username)

            if student is None:
                print(f"No student found with username {username}.")
            else:
                print(
                    f"ID: {student[0]}, "
                    f"Name: {student[1]}, "
                    f"Grade: {student[2]}"
                )

        except (psycopg.Error, ConnectionError) as error:
            print(f"Unable to retrieve student: {error}")

        break
