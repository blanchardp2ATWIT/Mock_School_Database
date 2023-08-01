import sqlite3
import tkinter as tk
from tkinter import messagebox

Current_Student_Amount = 10

menu_options ='''
1) Logout
2) Add/Remove Course From Semester Schedule
3) Assemble and print course Roster 
4) Add/Remove Courses from System
5) Search All Courses
6) Search Course By CRN Number
7) Quit
'''


def list_to_string(lst):
    return ', '.join(str(item) for item in lst)


def csv_string_to_list(csv_string):
    return [item.strip() for item in csv_string.split(',') if item.strip()]


def connect():
    try:
        return sqlite3.connect('assignment3.db')
    except sqlite3.Error:
        print("Could Not find .db File")


def print_table(cur, table):
    cur.execute("SELECT * FROM {}".format(table))
    r = cur.fetchall()
    for row in r:
        print(row)
    return


class User:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

    def print_available_classes(self, cursor):
        print("Here are the Available Classes this Semester:\n")
        cursor.execute("Select CRN, Title, department, time, days, semester, year, credits, instructor FROM COURSE")
        rows = cursor.fetchall()
        for row in rows:
            print(
                f"CRN:{row[0]} Title:{row[1]} Department:{row[2]} Time:{row[3]} Days:{row[4]} Semester:{row[5]} Year:{row[6]} Credits:{row[7]} Instructor:{row[8]}")

    def print_classes_from_crn(self, cursor, crn):
        print("Here are the Available Classes this Semester:\n")
        cursor.execute("Select CRN, Title, department, time, days, semester, year, credits, instructor FROM COURSE "
                       "WHERE CRN = '{}'".format(crn))
        rows = cursor.fetchall()
        for row in rows:
            print(
                f"CRN:{row[0]} Title:{row[1]} Department:{row[2]} Time:{row[3]} Days:{row[4]} Semester:{row[5]} Year:{row[6]} Credits:{row[7]} Instructor:{row[8]}")


class Student(User):
    def print_name(self):
        print("{} {}".format(self.firstname, self.lastname))

    def add_remove_course(self, cursor):
        action = input("Would you like to add or remove a course: ").lower()
        if action == 'add':
            crn_add = input("What is the CRN of the Course you would like to add: ")
            cursor.execute("SELECT CLASSES FROM STUDENT WHERE NAME = '{}'".format(self.firstname))
            current_classes = cursor.fetchone()[0]
            new_value = current_classes + crn_add + ","
            cursor.execute("UPDATE STUDENT SET CLASSES = '{}' WHERE NAME = '{}'".format(new_value, self.firstname))
        elif action == 'remove':
            crn_remove = input("What is the CRN of the Course you would like to remove: ")
            cursor.execute("SELECT CLASSES FROM STUDENT WHERE NAME = '{}'".format(self.firstname))
            current_classes = cursor.fetchone()[0]
            current_classes = current_classes.strip().split(',')
            new_class_list = []
            for classes in current_classes:
                if classes != crn_remove:
                    new_class_list.append(classes)
            new_class_list = list_to_string(new_class_list)
            cursor.execute("UPDATE STUDENT SET CLASSES = '{}' WHERE NAME = '{}'".format(new_class_list, self.firstname))


class Instructor(User):
    def print_name(self):
        print("{} {}".format(self.firstname, self.lastname))

    def class_list(self, cursor):
        students = []
        class_query = input("Input the CRN to the Class you would like the classlist for: ")
        cursor.execute("SELECT NAME, CLASSES FROM STUDENT")
        rows = cursor.fetchall()
        for row in rows:
            student_classes = csv_string_to_list(row[1])
            if class_query in student_classes:
                students.append(row[0])
        print(students)


class Admin(User):
    def print_name(self):
        print("{} {}".format(self.firstname, self.lastname))

    def add_remove_courses(self, cursor):
        action = input("Would you like to add or remove courses from the system: ").lower()
        if action == "add":
            crn_add = input("CRN of new Course: ")
            title = input("Title of new Course: ")
            department = input("Dept. of new Course: ")
            time = input("Time of new Course: ")
            days = input("Days of the Week(M,T,W,R,F) of new Course: ")
            semester = input("Semester of new Course: ")
            year = input("Year of new Course: ")
            creditss = input("Credits of new Course: ")
            instructor = input("Instructor of new Course: ")
            cursor.execute(
                "INSERT INTO COURSE VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(crn_add,
                                                                                                          title,
                                                                                                          department,
                                                                                                          time, days,
                                                                                                          semester,
                                                                                                          year,
                                                                                                          creditss,
                                                                                                          instructor))
            print(f"Successfully Added Course with CRN {crn_add}")
        elif action == 'remove':
            crn_remove = input("Input the CRN of the Class you would like to remove: ")
            cursor.execute(f"DELETE FROM COURSE WHERE CRN = '{crn_remove}")
            print(f"Successfully Deleted Course with CRN {crn_remove}")


def login(cursor):
    while 1:
        login_type = input("Are you a Student, Instructor or Admin: ").lower()
        if login_type == 'admin':
            user = input("Username:  ")
            password = input("Password: ")
            cursor.execute("Select NAME, SURNAME FROM ADMIN")
            rows = cursor.fetchall()
            for row in rows:
                col1 = row[0]
                col2 = row[1]
                if col1.lower() == user.lower():
                    if col2.lower() == password.lower():
                        print("Hello {} {} Welcome to Leopard Web".format(col1, col2))
                        return Admin(col1, col2)
            print("Unrecognized Login.\n")
        elif login_type == 'instructor':
            user = input("Username:  ")
            password = input("Password: ")
            cursor.execute("Select NAME, SURNAME FROM INSTRUCTOR")
            rows = cursor.fetchall()
            for row in rows:
                col1 = row[0]
                col2 = row[1]
                if col1.lower() == user.lower():
                    if col2.lower() == password.lower():
                        print("Hello {} {} Welcome to Leopard Web".format(col1, col2))
                        return Instructor(col1, col2)
            print("Unrecognized Login.\n")
        elif login_type == 'student':
            user = input("Username:  ")
            password = input("Password: ")
            cursor.execute("Select NAME, SURNAME FROM STUDENT")
            rows = cursor.fetchall()
            for row in rows:
                col1 = row[0]
                col2 = row[1]
                if col1.lower() == user.lower():
                    if col2.lower() == password.lower():
                        print("Hello {} {} Welcome to Leopard Web".format(col1, col2))
                        return Student(col1, col2)
            print("Unrecognized Login.\n")
        else:
            print("Invalid Input Try again")
            
def login_gui(sql_handle):
    def handle_login():
        login_type = login_type_var.get().lower()
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return

        cursor = sql_handle.cursor()
        if login_type == 'admin':
            cursor.execute("SELECT NAME, SURNAME FROM ADMIN")
        elif login_type == 'instructor':
            cursor.execute("SELECT NAME, SURNAME FROM INSTRUCTOR")
        elif login_type == 'student':
            cursor.execute("SELECT NAME, SURNAME FROM STUDENT")
        else:
            messagebox.showerror("Error", "Invalid login type.")
            return

        rows = cursor.fetchall()
        for row in rows:
            col1 = row[0]
            col2 = row[1]
            if col1.lower() == username.lower() and col2.lower() == password.lower():
                messagebox.showinfo("Success", f"Hello {col1} {col2}. Welcome to Leopard Web.")
                if login_type == 'admin':
                    user = Admin(col1, col2)
                elif login_type == 'instructor':
                    user = Instructor(col1, col2)
                elif login_type == 'student':
                    user = Student(col1, col2)

                root.destroy()
                main_program(user)
                return

        messagebox.showerror("Error", "Invalid username or password.")

    root = tk.Tk()
    root.title("Leopard Web Login")
    root.geometry("1000x500")

    login_type_var = tk.StringVar()
    login_type_var.set("student")

    login_type_label = tk.Label(root, text="Login Type:")
    login_type_label.pack()
    login_type_radio_student = tk.Radiobutton(root, text="Student", variable=login_type_var, value="student")
    login_type_radio_student.pack(anchor=tk.CENTER)
    login_type_radio_instructor = tk.Radiobutton(root, text="Instructor", variable=login_type_var, value="instructor")
    login_type_radio_instructor.pack(anchor=tk.CENTER)
    login_type_radio_admin = tk.Radiobutton(root, text="Admin", variable=login_type_var, value="admin")
    login_type_radio_admin.pack(anchor=tk.CENTER)

    username_label = tk.Label(root, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    password_label = tk.Label(root, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    login_button = tk.Button(root, text="Login", command=handle_login)
    login_button.pack()

    root.mainloop()
            
def main():
    sql_handle = connect()
    cur = sql_handle.cursor()
    login_gui(sql_handle)
    while 1:
        print("Welcome to Leopard Web Please login")
        user = login(cur)
        while 1:
            command = input(menu_options)
            if command == "1":
                break
            elif command == "2":
                user.add_remove_course(cur)
            elif command == "3":
                user.class_list(cur)
            elif command == "4":
                user.add_remove_courses(cur)
            elif command == "5":
                user.print_available_classes(cur)
            elif command == "6":
                temp = input("What is the CRN of the Class you are looking for: ")
                user.print_classes_from_crn(cur, temp)
            elif command == "7":
                sql_handle.commit()
                sql_handle.close()
                return


main()
