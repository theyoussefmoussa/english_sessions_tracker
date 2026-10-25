from database.connection import get_connection
def add_student(full_name, grade):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (full_name, grade) VALUES (%s, %s)", (full_name, grade))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Student {full_name} added successfully!")