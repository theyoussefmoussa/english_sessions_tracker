import re
from utils.constants import GRADES, MINIMUM_FULL_NAME_LENGTH

def validate_full_name():
    while True:
        full_name = input("Enter the student's full name: ").strip()

        parts = full_name.split()

        if len(full_name) < MINIMUM_FULL_NAME_LENGTH:
            print(f"Full name must be at least {MINIMUM_FULL_NAME_LENGTH} characters long.")
            continue

        # Check if the full name has at least two parts and contains only valid characters (letters, apostrophes, and hyphens)
        if len(parts) < 2 or not all(
            all(char.isalpha() or char in "'-" for char in part)
            for part in parts
        ):
            print("Enter a valid full name (first name and last name at minimum).")
            continue

        full_name = ' '.join(part.title() for part in parts)

        return full_name

def validate_grade():
    while True:
        grade = input("Enter the student's grade: ")
        # check if the grade is valid
        grade = grade.strip().capitalize() # to match the format in GRADES
        if grade not in GRADES:
            print(f"Grade must be one of the following: {', '.join(GRADES)}")
            continue
        return grade


def validate_student_username():
    while True:
        username = input("Enter the student's username: ").strip().lower()
        if not username:
            print("Username cannot be empty. Please try again.")
            continue
        if len(username) > 50:
            print("Username cannot exceed 50 characters. Please try again.")
            continue

        if not re.match(r'^[a-z0-9_]+$', username):
            print("Username can only contain lowercase letters, numbers, and underscores. Please try again.")
            continue
        return username


def validate_attendance_status():
    while True: 
        status = input("Enter the attendance status (Present/Absent): ").strip().capitalize()
        if status not in ['Present', 'Absent']:
            print("Status must be either 'Present' or 'Absent'. Please try again.")
            continue
        return status

from datetime import date

def validate_attendance_date():
    while True:
        print("1. Today's date")
        print("2. Enter a specific date (YYYY-MM-DD)")

        choice = input("Choose an option (1 or 2): ").strip()
        if choice == "1":
            return date.today()
        elif choice == "2":
            date_input = input("Enter the date (YYYY-MM-DD): ").strip()
            try:
                return date.fromisoformat(date_input)
            except ValueError:
                print("Invalid date. Please try again.")
        else:
            print("Invalid choice. Please choose 1 or 2.")