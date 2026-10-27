from students.operations import add_student, view_students

while True:
    print('-' * 50)
    print("Student Management System")
    print("1. Add Student")
    print("2. View Students")
    print('0. Exit')
    user_choice = input("Enter Your Choice: ")
    if user_choice == '0':
        print("Exiting the program.")
        break
    elif user_choice == '1':
        add_student()
    elif user_choice == '2':
        view_students()
    else: 
        print("Invalid choice. Please try again.")