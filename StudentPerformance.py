import numpy as np
import json
import csv


# ---------- Login ----------
def login():
    print("\nLogin Required")
    username = input("Username: ")
    password = input("Password: ")
    return username == "admin" and password == "admin123"


# ---------- Student ----------
class Student:
    def __init__(self, roll_no, name, english, maths, science, present):
        self.roll_no = roll_no
        self.name = name
        self.present = present
        self.marks = {
            "English": english,
            "Maths": maths,
            "Science": science
        }

    def percentage(self):
        if not self.present:
            return 0
        return round(np.mean(list(self.marks.values())), 2)


# ---------- Evaluation ----------
class EvaluatedStudent(Student):

    def grade(self):
        if not self.present:
            return "Absent"

        avg = self.percentage()

        if avg >= 85:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 50:
            return "C"
        else:
            return "F"

    def status(self):
        if not self.present:
            return "Absent on exam day"

        for mark in self.marks.values():
            if mark < 35:
                return "Better luck next time 😔"

        return "Good 👍"


# ---------- Analyzer ----------
class PerformanceAnalyzer:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    # Save records
    def save_records(self, filename="students.json"):
        data = []
        for s in self.students:
            data.append({
                "roll": s.roll_no,
                "name": s.name,
                "marks": s.marks,
                "present": s.present
            })

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f)

    # Export table report
    def export_report(self, filename="student_report.csv"):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            writer.writerow(
                ["Name", "Roll No", "Percentage", "Grade", "Status"]
            )

            for s in self.students:
                writer.writerow([
                    s.name,
                    s.roll_no,
                    s.percentage(),
                    s.grade(),
                    s.status()
                ])

    # Display table in notebook
    def show_table(self):
        if not self.students:
            print("No records available.")
            return

        print("\n===== STUDENT PERFORMANCE TABLE =====")
        print("-" * 90)
        print(f"{'Name':15}{'Roll No':10}{'Percentage':15}"
              f"{'Grade':12}{'Status':30}")
        print("-" * 90)

        for s in self.students:
            print(f"{s.name:15}{s.roll_no:<10}{s.percentage():<15}"
                  f"{s.grade():<12}{s.status():<30}")

        print("-" * 90)


# ---------- Program ----------
def run_program():

    if not login():
        print("Login Failed!")
        return

    analyzer = PerformanceAnalyzer()

    while True:
        print("\n===== MENU =====")
        print("1 Add Student")
        print("2 Show Records")
        print("3 Save Records")
        print("4 Export Report (Excel Table)")
        print("5 Exit")

        choice = input("Choice: ")

        if choice == "1":
            try:
                roll = int(input("Roll No: "))
                name = input("Name: ")

                present = input("Present in exam? (y/n): ").lower() == "y"

                if present:
                    english = float(input("English Marks: "))
                    maths = float(input("Maths Marks: "))
                    science = float(input("Science Marks: "))
                else:
                    english = maths = science = 0

                student = EvaluatedStudent(
                    roll, name, english, maths, science, present
                )

                analyzer.add_student(student)
                print("Record added successfully!")

            except ValueError:
                print("Invalid input!")

        elif choice == "2":
            analyzer.show_table()

        elif choice == "3":
            analyzer.save_records()
            print("Records saved.")

        elif choice == "4":
            analyzer.export_report()
            print("Report exported as Excel table.")

        elif choice == "5":
            print("Program closed.")
            break

        else:
            print("Invalid choice.")


# Run
run_program()