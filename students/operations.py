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

def get_students():
    conn = get_connection()

    # Check if the connection was successful 
    if conn is None:
        print("Unable to connect to the database. Please try again.")
        return None

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT student_id, full_name, grade FROM students ORDER BY student_id;")
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
            print(f"ID: {student[0]}, Name: {student[1]}, Grade: {student[2]}")
    else:
        print("No students found.")

def get_student_by_id(student_id):
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
                    WHERE student_id = %s
                    """,
                    (student_id,)
                )
                return cur.fetchone()
    finally:
        conn.close()

def view_student_by_id():
    while True:
        student_id = input("Enter the student's ID: ").strip()

        if not student_id.isdigit():
            print("Invalid ID. Please enter a numeric value.")
            continue

        try:
            student = get_student_by_id(int(student_id))

            if student is None:
                print(f"No student found with ID {student_id}.")
            else:
                print(
                    f"ID: {student[0]}, "
                    f"Name: {student[1]}, "
                    f"Grade: {student[2]}"
                )

        except (psycopg.Error, ConnectionError) as error:
            print(f"Unable to retrieve student: {error}")

        break