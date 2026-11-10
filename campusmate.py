from abc import ABC, abstractmethod


# Grade scale stored as a tuple
GRADE_SCALE = (
    (90, "A+"),
    (80, "A"),
    (70, "B"),
    (60, "C"),
    (50, "D"),
    (0, "F")
)


# 1. Parent class
class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age


# 2. Student inherits from Person
class Student(Person):

    def __init__(self, student_id, name, age, course):
        super().__init__(name, age)

        self.student_id = student_id
        self.course = course

        # Private attributes (Encapsulation)
        self.__marks = {}
        self.__attendance = 0

    # Getter for marks
    def get_marks(self):
        return self.__marks.copy()

    # Add or update marks
    def add_marks(self, subject, marks):

        if marks < 0 or marks > 100:
            print("Marks must be between 0 and 100.")
            return False

        self.__marks[subject.title()] = marks
        return True

    # Getter for attendance
    def get_attendance(self):
        return self.__attendance

    # Setter for attendance
    def set_attendance(self, attendance):

        if attendance < 0 or attendance > 100:
            print("Attendance must be between 0 and 100.")
            return False

        self.__attendance = attendance
        return True

    # Calculate average marks
    def calculate_average(self):

        if len(self.__marks) == 0:
            return 0

        total = sum(self.__marks.values())
        return total / len(self.__marks)

    # Calculate grade
    def calculate_grade(self):

        average = self.calculate_average()

        for minimum, grade in GRADE_SCALE:
            if average >= minimum:
                return grade

    # Overridden method
    def role(self):
        return "Student"


# 3. Abstract class
class Report(ABC):

    @abstractmethod
    def generate(self, student):
        pass


# 4. Academic report
class AcademicReport(Report):

    def generate(self, student):

        print("\n========== ACADEMIC REPORT ==========")

        print("Student ID:", student.student_id)
        print("Name:", student.name)
        print("Course:", student.course)

        marks = student.get_marks()

        if len(marks) == 0:
            print("No marks have been entered.")
            return

        for subject, score in marks.items():
            print(subject + ":", score, "/ 100")

        print("Average:", round(
            student.calculate_average(), 2))

        print("Grade:", student.calculate_grade())

        print("=====================================")


# 5. Attendance report
class AttendanceReport(Report):

    def generate(self, student):

        attendance = student.get_attendance()

        print("\n========= ATTENDANCE REPORT =========")
        print("Student:", student.name)
        print("Attendance:", attendance, "%")

        if attendance >= 75:
            print("Status: Eligible")
        else:
            print("Status: Attendance below 75%")

        print("=====================================")


# 6. Main management system
class CampusMate:

    def __init__(self):
        self.__students = []

    # Find student using ID
    def find_student(self, student_id):

        for student in self.__students:
            if student.student_id == student_id:
                return student

        return None

    # Add student
    def add_student(self):

        print("\n------ ADD NEW STUDENT ------")

        student_id = input("Enter student ID: ").strip()

        if student_id == "":
            print("Student ID cannot be empty.")
            return

        if self.find_student(student_id) is not None:
            print("Student ID already exists.")
            return

        name = input("Enter student name: ").strip()

        if name == "":
            print("Name cannot be empty.")
            return

        try:
            age = int(input("Enter age: "))

            if age <= 0:
                print("Age must be positive.")
                return

        except ValueError:
            print("Enter a valid age.")
            return

        course = input("Enter course: ").strip()

        if course == "":
            print("Course cannot be empty.")
            return

        student = Student(
            student_id, name.title(), age, course.upper()
        )

        self.__students.append(student)

        print("Student added successfully!")

    # Display all students
    def view_students(self):

        print("\n------ STUDENT RECORDS ------")

        if len(self.__students) == 0:
            print("No student records found.")
            return

        for student in self.__students:

            print("\nID:", student.student_id)
            print("Name:", student.name)
            print("Age:", student.age)
            print("Course:", student.course)
            print("Role:", student.role())

    # Add marks
    def add_marks(self):

        student_id = input("Enter student ID: ").strip()
        student = self.find_student(student_id)

        if student is None:
            print("Student not found.")
            return

        subject = input("Enter subject: ").strip()

        if subject == "":
            print("Subject cannot be empty.")
            return

        try:
            marks = float(input("Enter marks out of 100: "))

        except ValueError:
            print("Enter valid numeric marks.")
            return

        if student.add_marks(subject, marks):
            print("Marks saved successfully!")

    # Update attendance
    def update_attendance(self):

        student_id = input("Enter student ID: ").strip()
        student = self.find_student(student_id)

        if student is None:
            print("Student not found.")
            return

        try:
            attendance = float(
                input("Enter attendance percentage: ")
            )

        except ValueError:
            print("Enter a valid number.")
            return

        if student.set_attendance(attendance):
            print("Attendance updated successfully!")

    # Generate reports
    def generate_report(self):

        student_id = input("Enter student ID: ").strip()
        student = self.find_student(student_id)

        if student is None:
            print("Student not found.")
            return

        academic = AcademicReport()
        attendance = AttendanceReport()

        print("\n1. Academic Report")
        print("2. Attendance Report")
        print("3. Complete Report")

        choice = input("Enter choice: ")

        # Polymorphism:
        # Both report objects use the same method name.
        reports = []

        if choice == "1":
            reports = [academic]

        elif choice == "2":
            reports = [attendance]

        elif choice == "3":
            reports = [academic, attendance]

        else:
            print("Invalid choice.")
            return

        for report in reports:
            report.generate(student)

    # Search student
    def search_student(self):

        student_id = input("Enter student ID: ").strip()
        student = self.find_student(student_id)

        if student is None:
            print("Student not found.")
        else:
            print("\nStudent found!")
            print("Name:", student.name)
            print("Course:", student.course)
            print("Average:", round(
                student.calculate_average(), 2
            ))

    # Delete student
    def delete_student(self):

        student_id = input("Enter student ID: ").strip()

        student = self.find_student(student_id)

        if student is None:
            print("Student not found.")
            return

        self.__students.remove(student)
        print("Student record deleted.")

    # Class summary
    def class_summary(self):

        if len(self.__students) == 0:
            print("No student records available.")
            return

        # Set stores unique subjects
        subjects = set()

        topper = None

        for student in self.__students:

            for subject in student.get_marks():
                subjects.add(subject)

            if student.get_marks():

                if topper is None:
                    topper = student

                elif (student.calculate_average() >
                      topper.calculate_average()):
                    topper = student

        print("\n========== CLASS SUMMARY ==========")

        print("Total Students:", len(self.__students))

        print("Subjects:", ", ".join(sorted(subjects))
              if subjects else "No subjects added")

        if topper is not None:
            print("Topper:", topper.name)
            print("Average Marks:",
                  round(topper.calculate_average(), 2))
        else:
            print("No marks available yet.")

        print("====================================")


# 7. Main function
def main():

    system = CampusMate()

    while True:

        print("\n")
        print("====================================")
        print("          CAMPUSMATE")
        print("     STUDENT MANAGEMENT SYSTEM")
        print("====================================")

        print("1. Add Student")
        print("2. View All Students")
        print("3. Add Subject Marks")
        print("4. Update Attendance")
        print("5. Generate Student Report")
        print("6. Search Student")
        print("7. Delete Student")
        print("8. Class Summary")
        print("9. Exit")

        print("====================================")

        choice = input("Enter your choice (1-9): ")

        if choice == "1":
            system.add_student()

        elif choice == "2":
            system.view_students()

        elif choice == "3":
            system.add_marks()

        elif choice == "4":
            system.update_attendance()

        elif choice == "5":
            system.generate_report()

        elif choice == "6":
            system.search_student()

        elif choice == "7":
            system.delete_student()

        elif choice == "8":
            system.class_summary()

        elif choice == "9":
            print("Thank you for using CampusMate!")
            break

        else:
            print("Invalid choice. Please try again.")


# Program execution
if __name__ == "__main__":
    main()
