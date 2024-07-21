class User:
    def __init__(self, user_id, username, password, full_name, email):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email


class Doctor(User):
    def __init__(self, user_id, username, password, full_name, email):
        super().__init__(user_id, username, password, full_name, email)
        self.courses = []

    def create_course(self, course_name, course_code):
        course = Course(course_name, course_code, self)
        self.courses.append(course)
        print(f"Course '{course_name}' created successfully!")

    def create_assignment(self, course_code, title, description):
        course = next((c for c in self.courses if c.code == course_code), None)
        if course:
            course.create_assignment(title, description)
        else:
            print(f"Course with code '{course_code}' not found.")

class Student(User):
    def __init__(self, user_id, username, password, full_name, email):
        super().__init__(user_id, username, password, full_name, email)
        self.courses = []

    def register_course(self, course):
        if course not in self.courses:
            self.courses.append(course)
            course.students.append(self)
            print(f"You registered in course '{course.name}' successfully!")

class TA(User):
    def __init__(self, user_id, username, password, full_name, email):
        super().__init__(user_id, username, password, full_name, email)
        self.courses = []

    def TA_courses(self, course):
        if course not in self.courses:
            self.courses.append(course)
            print(f"TA assigned to course '{course.name}' successfully!")

class Course:
    def __init__(self, name, code, doctor):
        self.name = name
        self.code = code
        self.doctor = doctor
        self.students = []
        self.assignments = []

    def create_assignment(self, title, description):
        assignment = Assignment(title, description, self)
        self.assignments.append(assignment)
        print(f"The assignment '{title}' created successfully ")

class Assignment:
    def __init__(self, title, description, course):
        self.title = title
        self.description = description
        self.course = course
        self.solutions = {}

    def submit_solution(self, student, solution):
        self.solutions[student] = solution
        print(f"Solution submitted for assignment '{self.title}' by '{student.username}'")

    def grade_solution(self, student, grade):
        if student in self.solutions:
            self.solutions[student]['grade'] = grade
            print(f"Solution graded  for student '{student.username}' with grade '{grade}'")
            
def main():
    users = []
    courses = []

    while True:
        print("1. Sign Up")
        print("2. Sign In")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            print("1. Doctor")
            print("2. Student")
            print("3. TA")
            user_type = input("Enter user type: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            full_name = input("Enter full name: ")
            email = input("Enter email: ")
            user_id = len(users) + 1

            if user_type == '1':
                user = Doctor(user_id, username, password, full_name, email)
            elif user_type == '2':
                user = Student(user_id, username, password, full_name, email)
            elif user_type == '3':
                user = TA(user_id, username, password, full_name, email)
            else:
                print("Enter a valid user type")
                continue

            users.append(user)
            print(f"User '{username}' signed up successfully!")

        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            user = None
            for u in users:
                if u.username == username and u.password == password:
                    user = u
                    break

            if user:
                print(f"Welcome {user.full_name}!")
                while True:
                    if isinstance(user, Doctor):
                        print("1. Create Course")
                        print("2. Create Assignment")  # Added option
                        print("3. View Courses")
                        print("4. Log Out")
                        doctor_choice = input("Enter choice: ")

                        if doctor_choice == '1':
                            course_name = input("Enter course name: ")
                            course_code = input("Enter course code: ")
                            user.create_course(course_name, course_code)
                            courses.append(user.courses[-1])
                        elif doctor_choice == '2':
                            course_code = input("Enter course code to add assignment to: ")
                            title = input("Enter assignment title: ")
                            description = input("Enter assignment description: ")
                            user.create_assignment(course_code, title, description)
                        elif doctor_choice == '3':
                            for course in user.courses:
                                print(f"Course: {course.name}, Code: {course.code}")
                        elif doctor_choice == '4':
                            break
                        else:
                            print("Invalid choice")

                    elif isinstance(user, Student):
                        print("1. Register Course")
                        print("2. View My Courses")
                        print("3. Log Out")
                        student_choice = input("Enter choice: ")

                        if student_choice == '1':
                            for course in courses:
                                if user not in course.students:
                                    print(f"Course: {course.name}, Code: {course.code}")
                            course_code = input("Enter course code to register: ")
                            course = None
                            for c in courses:
                                if c.code == course_code:
                                    course = c
                                    break
                            if course:
                                user.register_course(course)
                            else:
                                print("Invalid course code")
                        elif student_choice == '2':
                            for course in user.courses:
                                print(f"Course: {course.name}, Code: {course.code}")
                        elif student_choice == '3':
                            break
                        else:
                            print("Invalid choice")

                    elif isinstance(user, TA):
                        print("1. Assign to Course")
                        print("2. View My Courses")
                        print("3. Log Out")
                        ta_choice = input("Enter choice: ")

                        if ta_choice == '1':
                            for course in courses:
                                if user not in course.students:
                                    print(f"Course: {course.name}, Code: {course.code}")
                            course_code = input("Enter course code to assign: ")
                            course = None
                            for c in courses:
                                if c.code == course_code:
                                    course = c
                                    break
                            if course:
                                user.TA_courses(course)
                            else:
                                print("Invalid course code")
                        elif ta_choice == '2':
                            for course in user.courses:
                                print(f"Course: {course.name}, Code: {course.code}")
                        elif ta_choice == '3':
                            break
                        else:
                            print("Invalid choice")
            else:
                print("Invalid data")

        elif choice == '3':
            break

        else:
            print("Please enter a valid number")

main()

