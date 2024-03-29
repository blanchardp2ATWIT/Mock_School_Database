import sqlite3

Current_Student_Amount = 10

menu_options = '''
1) Logout
2) Add/Remove Course From Semester Schedule
3) Assemble and print course Roster 
4) Add/Remove Courses from System
5) Search All Courses
6) Search Course By CRN Number
7) Adjust Student Schedule
8) Add User
9) Quit
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

    def add_user(self, cursor):
        table = input("Which type of user would you like to add, Admin, Instructor or Student: ").lower()
        if table == "instructor":
            eye_dee = input("ID of the new Instructor: ")
            name = input("Name of the new Instructor: ")
            Surname = input("Surname of the new Instructor")
            Title = input("Title of the new Instructor: ")
            hireyear = input("When was the Instructor hired: ")
            department = input("Department of the new Instructor: ")
            email = input("Email of the new Instructor: ")
            cursor.execute(
                "INSERT INTO INSTRUCTOR VALUES ('{}', '{}', '{}', '{}', '{}', '{}','{}')".format(eye_dee, name, Surname,
                                                                                                 Title, hireyear,
                                                                                                 department, email))
        elif table == "student":
            eye_dee = input("ID of the new student: ")
            name = input("Name of the new student: ")
            Surname = input("Surname of the new student")
            gradyear = input("Grad year of Student: ")
            department = input("Department of the new student: ")
            classes = input(",")
            cursor.execute(
                "INSERT INTO STUDENT VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(eye_dee, name, Surname,
                                                                                                 gradyear, department,classes))

        elif table == "admin":
            eye_dee = input("ID of the new Admin: ")
            name = input("Name of the new Admin: ")
            Surname = input("Surname of the new Admin")
            Title = input("Title of Admin: ")
            Office = input("Office of the new Admin: ")
            email = Surname + name[0]
            cursor.execute(
                "INSERT INTO ADMIN VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(eye_dee, name, Surname,
                                                                                         Title, Office, email))

    def add_remove_student_course(self, cursor):
        action = input("Would you like to add or remove a course: ").lower()
        eye_dee = input("What is the students ID")
        if action == 'add':
            crn_add = input("What is the CRN of the Course you would like to add: ")
            cursor.execute("SELECT CLASSES FROM STUDENT WHERE ID = '{}'".format(eye_dee))
            current_classes = cursor.fetchone()[0]
            new_value = current_classes + crn_add + ","
            cursor.execute("UPDATE STUDENT SET CLASSES = '{}' WHERE ID = '{}'".format(new_value, eye_dee))
        elif action == 'remove':
            crn_remove = input("What is the CRN of the Course you would like to remove: ")
            cursor.execute("SELECT CLASSES FROM STUDENT WHERE ID = '{}'".format(eye_dee))
            current_classes = cursor.fetchone()[0]
            current_classes = current_classes.strip().split(',')
            new_class_list = []
            for classes in current_classes:
                if classes != crn_remove:
                    new_class_list.append(classes)
            new_class_list = list_to_string(new_class_list)
            cursor.execute("UPDATE STUDENT SET CLASSES = '{}' WHERE ID = '{}'".format(new_class_list, eye_dee))

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


def main():
    sql_handle = connect()
    cur = sql_handle.cursor()
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
                user.add_remove_student_course(cur)
            elif command == "8":
                user.add_user(cur)
            elif command == "9":
                sql_handle.commit()
                sql_handle.close()
                return


main()
