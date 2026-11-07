import psycopg

from database.connection import get_connection
from src.repository import get_students


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
