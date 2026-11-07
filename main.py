from src.attendance_op import mark_attendance, view_attendance
from src.view import view_students, view_student_by_username
from src.repository import add_student
while True:
    print('-' * 50)
    print("Student Management System")
    print("1. Add Student")
    print("2. View Students")
    print('3. View Student by Username')
    print('4. Mark Attendance')
    print('5. View Attendance')
    print('0. Exit')
    user_choice = input("Enter Your Choice: ")
    if user_choice == '0':
        print("Exiting the program.")
        break
    elif user_choice == '1':
        add_student()
    elif user_choice == '2':
        view_students()
    elif user_choice == '3':
        view_student_by_username()
    elif user_choice == '4':
        mark_attendance()
    elif user_choice == '5':
        view_attendance()
    else: 
        print("Invalid choice. Please try again.")