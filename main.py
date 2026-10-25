import psycopg
from database.connection import get_connection
from students.operations import add_student

while True:
    print("Student Management System")
    print("1. Add Student")
    print('0. Exit')
    user_choice = input("Enter Your Choice: ")
    if user_choice == '0':
        print("Exiting the program.")
        break
    elif user_choice == '1':
        full_name = input("Enter Full Name: ")
        grade = input("Enter Grade (Fundamentals, Grade 1, Grade 2, Grade 3, Grade 4, Grade 5, Grade 6, Grade 7):")
        add_student(full_name, grade)