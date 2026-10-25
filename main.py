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
        add_student()
    else: 
        print("Invalid choice. Please try again.")