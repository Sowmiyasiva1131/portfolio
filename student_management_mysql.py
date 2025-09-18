import sqlite3

# ---------------- OOP Classes ----------------
class Student:
    def __init__(self, student_id, name, age, grades):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grades = grades  # list of floats

    def average_grade(self):
        if self.grades:
            return sum(self.grades)/len(self.grades)
        return 0

class StudentManagerDB:
    def __init__(self, db_name="students.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            grades TEXT
        )
        """)
        self.conn.commit()

    def add_student(self, student):
        grades_str = ','.join(map(str, student.grades))
        self.cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?)",
                            (student.student_id, student.name, student.age, grades_str))
        self.conn.commit()
        print(f"Student {student.name} added successfully.")

    def remove_student(self, student_id):
        self.cursor.execute("DELETE FROM students WHERE student_id=?", (student_id,))
        self.conn.commit()
        print(f"Student with ID {student_id} removed successfully.")

    def get_all_students(self):
        self.cursor.execute("SELECT * FROM students")
        rows = self.cursor.fetchall()
        students = []
        for row in rows:
            student_id, name, age, grades_str = row
            grades = list(map(float, grades_str.split(','))) if grades_str else []
            students.append(Student(student_id, name, age, grades))
        return students

    def generate_html(self):
        students = self.get_all_students()
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Student Management</title>
            <style>
                body { font-family: Arial, sans-serif; background: #f0f0f0; padding: 20px;}
                table { width: 70%; border-collapse: collapse; margin: auto; background: #fff;}
                th, td { padding: 12px; border: 1px solid #ddd; text-align: center;}
                th { background: #7e22ce; color: white;}
                tr:nth-child(even) { background: #f9f9f9;}
            </style>
        </head>
        <body>
            <h2 style="text-align:center;">Student Management System</h2>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Age</th>
                    <th>Grades</th>
                    <th>Average</th>
                </tr>
        """
        for s in students:
            html_content += f"""
                <tr>
                    <td>{s.student_id}</td>
                    <td>{s.name}</td>
                    <td>{s.age}</td>
                    <td>{', '.join(map(str, s.grades))}</td>
                    <td>{s.average_grade():.2f}</td>
                </tr>
            """
        html_content += """
            </table>
        </body>
        </html>
        """
        with open("students.html", "w") as f:
            f.write(html_content)
        print("HTML file updated: students.html")

# ---------------- Interactive Menu ----------------
manager = StudentManagerDB()

while True:
    print("\n--- Student Management System (SQL) ---")
    print("1. Add Student")
    print("2. Remove Student")
    print("3. Generate HTML")
    print("4. Show Students in Console")
    print("5. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        sid = int(input("Enter Student ID: "))
        name = input("Enter Name: ")
        age = int(input("Enter Age: "))
        grades = list(map(float, input("Enter grades separated by commas: ").split(',')))
        manager.add_student(Student(sid, name, age, grades))

    elif choice == '2':
        sid = int(input("Enter Student ID to remove: "))
        manager.remove_student(sid)

    elif choice == '3':
        manager.generate_html()
        print("Open 'students.html' in your browser to view students.")

    elif choice == '4':
        students = manager.get_all_students()
        for s in students:
            print(f"{s.student_id} - {s.name} - Age: {s.age} - Grades: {s.grades} - Avg: {s.average_grade():.2f}")

    elif choice == '5':
        print("Exiting system...")
        break

    else:
        print("Invalid choice! Please try again.")
