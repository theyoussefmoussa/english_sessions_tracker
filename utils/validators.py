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