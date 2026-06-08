from tkinter import *
from tkinter import messagebox
import json
import os

students = []

# Grade Function
def get_grade(marks):
    marks = int(marks)

    if marks >= 90:
        return "A"
    elif marks >= 75:
        return "B"
    elif marks >= 50:
        return "C"
    else:
        return "D"

# Save Data
def save_data():
    with open("students.json", "w") as file:
        json.dump(students, file)

# Load Data
def load_data():
    global students

    if os.path.exists("students.json"):
        with open("students.json", "r") as file:
            students = json.load(file)

        update_list()

# Update Listbox
def update_list():
    listbox.delete(0, END)

    for student in students:
        listbox.insert(
            END,
            f"{student['name']} | Marks: {student['marks']} | Grade: {student['grade']}"
        )

    count_label.config(text=f"Total Students: {len(students)}")

# Add Student
def add_student():
    name = name_entry.get()
    marks = marks_entry.get()

    if name == "" or marks == "":
        messagebox.showwarning("Warning", "Enter all details!")
        return

    try:
        marks = int(marks)
    except:
        messagebox.showerror("Error", "Marks must be number!")
        return

    student = {
        "name": name,
        "marks": marks,
        "grade": get_grade(marks)
    }

    students.append(student)

    save_data()
    update_list()

    name_entry.delete(0, END)
    marks_entry.delete(0, END)

# Delete Student
def delete_student():
    selected = listbox.curselection()

    if not selected:
        messagebox.showwarning("Warning", "Select student!")
        return

    students.pop(selected[0])

    save_data()
    update_list()

# Select Student
def select_student(event):
    selected = listbox.curselection()

    if selected:
        index = selected[0]

        name_entry.delete(0, END)
        marks_entry.delete(0, END)

        name_entry.insert(0, students[index]["name"])
        marks_entry.insert(0, students[index]["marks"])

# Edit Student
def edit_student():
    selected = listbox.curselection()

    if not selected:
        messagebox.showwarning("Warning", "Select student!")
        return

    index = selected[0]

    name = name_entry.get()
    marks = int(marks_entry.get())

    students[index] = {
        "name": name,
        "marks": marks,
        "grade": get_grade(marks)
    }

    save_data()
    update_list()

# Search Student
def search_student():
    keyword = name_entry.get().lower()

    listbox.delete(0, END)

    for student in students:
        if keyword in student["name"].lower():
            listbox.insert(
                END,
                f"{student['name']} | Marks: {student['marks']} | Grade: {student['grade']}"
            )

# GUI
root = Tk()
root.title("Student Management System")
root.geometry("650x500")

Label(root, text="Student Name").pack(pady=5)
name_entry = Entry(root, width=40)
name_entry.pack()

Label(root, text="Marks").pack(pady=5)
marks_entry = Entry(root, width=40)
marks_entry.pack()

Button(root, text="Add Student", command=add_student).pack(pady=3)
Button(root, text="Edit Student", command=edit_student).pack(pady=3)
Button(root, text="Delete Student", command=delete_student).pack(pady=3)
Button(root, text="Search Student", command=search_student).pack(pady=3)

listbox = Listbox(root, width=70, height=12)
listbox.pack(pady=10)
listbox.bind("<<ListboxSelect>>", select_student)

count_label = Label(root, text="Total Students: 0")
count_label.pack()

load_data()

root.mainloop()