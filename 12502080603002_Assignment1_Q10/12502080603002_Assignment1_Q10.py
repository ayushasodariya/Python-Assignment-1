import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import os


DATA_FILE = "assignment_data.json"

students = {}
submissions = []


# Load previously saved data when the program starts
def load_data():
    global students, submissions

    if not os.path.exists(DATA_FILE):
        return

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        students = data.get("students", {})
        submissions = data.get("submissions", [])

    except (json.JSONDecodeError, OSError):
        messagebox.showwarning(
            "Warning",
            "Saved data could not be loaded. Starting with empty data."
        )


# Save current data to JSON
def save_data():
    data = {
        "students": students,
        "submissions": submissions
    }

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except OSError as error:
        messagebox.showerror("Error", f"Could not save data:\n{error}")


def add_student():
    enrollment = enrollment_entry.get().strip()
    name = name_entry.get().strip()

    if not enrollment or not name:
        messagebox.showerror("Invalid Input", "Enter enrollment number and name.")
        return

    if not enrollment.isdigit():
        messagebox.showerror("Invalid Input", "Enrollment number must contain digits only.")
        return

    if enrollment in students:
        messagebox.showerror("Duplicate", "Student already exists.")
        return

    students[enrollment] = name

    update_student_list()
    save_data()

    enrollment_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)

    messagebox.showinfo("Success", "Student added successfully.")


def update_student_list():
    student_values = [
        f"{enrollment} - {name}"
        for enrollment, name in sorted(students.items())
    ]

    student_combo["values"] = student_values


def add_submission():
    selected_student = student_combo.get().strip()
    assignment = assignment_entry.get().strip()
    marks_text = marks_entry.get().strip()
    max_marks_text = max_marks_entry.get().strip()
    remarks = remarks_entry.get().strip()

    if not selected_student or not assignment:
        messagebox.showerror(
            "Invalid Input",
            "Select a student and enter assignment name."
        )
        return

    if not marks_text or not max_marks_text:
        messagebox.showerror(
            "Invalid Input",
            "Enter marks and maximum marks."
        )
        return

    try:
        marks = float(marks_text)
        max_marks = float(max_marks_text)
    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Marks must be numeric."
        )
        return

    if max_marks <= 0:
        messagebox.showerror(
            "Invalid Input",
            "Maximum marks must be greater than zero."
        )
        return

    if marks < 0 or marks > max_marks:
        messagebox.showerror(
            "Invalid Input",
            "Marks must be between 0 and maximum marks."
        )
        return

    enrollment = selected_student.split(" - ")[0]
    name = students[enrollment]

    status = status_var.get()

    submission = {
        "enrollment": enrollment,
        "name": name,
        "assignment": assignment,
        "status": status,
        "marks": marks,
        "max_marks": max_marks,
        "remarks": remarks
    }

    submissions.append(submission)

    save_data()
    refresh_table()

    assignment_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)
    max_marks_entry.delete(0, tk.END)
    remarks_entry.delete(0, tk.END)

    messagebox.showinfo("Success", "Submission added successfully.")


def update_marks():
    selected = table.selection()

    if not selected:
        messagebox.showerror(
            "Selection Required",
            "Select a submission from the table first."
        )
        return

    index = int(selected[0])

    marks_text = marks_entry.get().strip()
    max_marks_text = max_marks_entry.get().strip()

    try:
        marks = float(marks_text)
        max_marks = float(max_marks_text)
    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Enter valid numeric marks."
        )
        return

    if max_marks <= 0 or marks < 0 or marks > max_marks:
        messagebox.showerror(
            "Invalid Input",
            "Marks must be between 0 and maximum marks."
        )
        return

    submissions[index]["marks"] = marks
    submissions[index]["max_marks"] = max_marks
    submissions[index]["status"] = status_var.get()
    submissions[index]["remarks"] = remarks_entry.get().strip()

    save_data()
    refresh_table()

    messagebox.showinfo("Updated", "Submission updated successfully.")


def load_selected_submission(event=None):
    selected = table.selection()

    if not selected:
        return

    index = int(selected[0])
    record = submissions[index]

    assignment_entry.delete(0, tk.END)
    assignment_entry.insert(0, record["assignment"])

    marks_entry.delete(0, tk.END)
    marks_entry.insert(0, record["marks"])

    max_marks_entry.delete(0, tk.END)
    max_marks_entry.insert(0, record["max_marks"])

    remarks_entry.delete(0, tk.END)
    remarks_entry.insert(0, record["remarks"])

    status_var.set(record["status"])

    student_combo.set(
        f"{record['enrollment']} - {record['name']}"
    )


def refresh_table():
    for item in table.get_children():
        table.delete(item)

    selected_filter = filter_var.get()

    for index, record in enumerate(submissions):

        if selected_filter != "All":
            if record["status"] != selected_filter:
                continue

        table.insert(
            "",
            tk.END,
            iid=str(index),
            values=(
                record["enrollment"],
                record["name"],
                record["assignment"],
                record["status"],
                format_marks(record["marks"]),
                format_marks(record["max_marks"]),
                record["remarks"]
            )
        )


def format_marks(value):
    if float(value).is_integer():
        return str(int(value))
    return str(value)


def export_csv():
    if not submissions:
        messagebox.showwarning(
            "No Data",
            "There are no submissions to export."
        )
        return

    file_path = filedialog.asksaveasfilename(
        title="Save CSV Report",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")]
    )

    if not file_path:
        return

    try:
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Enrollment",
                "Name",
                "Assignment",
                "Status",
                "Marks",
                "Remarks"
            ])

            for record in submissions:
                writer.writerow([
                    record["enrollment"],
                    record["name"],
                    record["assignment"],
                    record["status"],
                    format_marks(record["marks"]),
                    record["remarks"]
                ])

        messagebox.showinfo(
            "Export Complete",
            f"CSV report saved successfully."
        )

    except OSError as error:
        messagebox.showerror(
            "Export Error",
            str(error)
        )


def change_filter(event=None):
    refresh_table()


# ---------------- GUI ----------------

root = tk.Tk()
root.title("Assignment Tracker")
root.geometry("1000x650")
root.minsize(850, 550)


title_label = tk.Label(
    root,
    text="Student Assignment Tracker",
    font=("Arial", 20, "bold")
)
title_label.pack(pady=10)


# Student section
student_frame = tk.LabelFrame(
    root,
    text="Add Student",
    padx=10,
    pady=10
)
student_frame.pack(fill="x", padx=15, pady=5)

tk.Label(student_frame, text="Enrollment").grid(
    row=0, column=0, padx=5, pady=5
)

enrollment_entry = tk.Entry(student_frame, width=20)
enrollment_entry.grid(row=0, column=1, padx=5)


tk.Label(student_frame, text="Name").grid(
    row=0, column=2, padx=5
)

name_entry = tk.Entry(student_frame, width=25)
name_entry.grid(row=0, column=3, padx=5)


add_student_button = tk.Button(
    student_frame,
    text="Add Student",
    command=add_student
)
add_student_button.grid(row=0, column=4, padx=10)


# Submission section
submission_frame = tk.LabelFrame(
    root,
    text="Assignment Submission",
    padx=10,
    pady=10
)
submission_frame.pack(fill="x", padx=15, pady=5)


tk.Label(submission_frame, text="Student").grid(
    row=0, column=0, padx=5, pady=5
)

student_combo = ttk.Combobox(
    submission_frame,
    width=23,
    state="readonly"
)
student_combo.grid(row=0, column=1, padx=5)


tk.Label(submission_frame, text="Assignment").grid(
    row=0, column=2, padx=5
)

assignment_entry = tk.Entry(
    submission_frame,
    width=20
)
assignment_entry.grid(row=0, column=3, padx=5)


tk.Label(submission_frame, text="Marks").grid(
    row=1, column=0, padx=5, pady=5
)

marks_entry = tk.Entry(
    submission_frame,
    width=10
)
marks_entry.grid(row=1, column=1, padx=5, sticky="w")


tk.Label(submission_frame, text="Max Marks").grid(
    row=1, column=2, padx=5
)

max_marks_entry = tk.Entry(
    submission_frame,
    width=10
)
max_marks_entry.grid(row=1, column=3, padx=5, sticky="w")


tk.Label(submission_frame, text="Remarks").grid(
    row=2, column=0, padx=5, pady=5
)

remarks_entry = tk.Entry(
    submission_frame,
    width=45
)
remarks_entry.grid(
    row=2,
    column=1,
    columnspan=3,
    padx=5,
    sticky="w"
)


# Radio buttons for submission status
status_var = tk.StringVar(value="Pending")

tk.Label(submission_frame, text="Status").grid(
    row=3, column=0, padx=5, pady=5
)

tk.Radiobutton(
    submission_frame,
    text="Pending",
    variable=status_var,
    value="Pending"
).grid(row=3, column=1, sticky="w")

tk.Radiobutton(
    submission_frame,
    text="Completed",
    variable=status_var,
    value="Completed"
).grid(row=3, column=2, sticky="w")


add_submission_button = tk.Button(
    submission_frame,
    text="Add Submission",
    command=add_submission
)
add_submission_button.grid(row=4, column=1, pady=8)


update_button = tk.Button(
    submission_frame,
    text="Update Selected",
    command=update_marks
)
update_button.grid(row=4, column=2, pady=8)


# Filter
filter_frame = tk.Frame(root)
filter_frame.pack(fill="x", padx=15, pady=8)

tk.Label(
    filter_frame,
    text="Filter:"
).pack(side="left", padx=5)

filter_var = tk.StringVar(value="All")

filter_combo = ttk.Combobox(
    filter_frame,
    textvariable=filter_var,
    values=["All", "Pending", "Completed"],
    state="readonly",
    width=15
)
filter_combo.pack(side="left", padx=5)
filter_combo.bind("<<ComboboxSelected>>", change_filter)


export_button = tk.Button(
    filter_frame,
    text="Export CSV",
    command=export_csv
)
export_button.pack(side="right", padx=5)


# Table
table_frame = tk.Frame(root)
table_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=5
)

columns = (
    "Enrollment",
    "Name",
    "Assignment",
    "Status",
    "Marks",
    "Max Marks",
    "Remarks"
)

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

for column in columns:
    table.heading(column, text=column)
    table.column(column, width=110)

table.column("Remarks", width=180)

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=table.yview
)

table.configure(yscrollcommand=scrollbar.set)

table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

table.bind("<<TreeviewSelect>>", load_selected_submission)


# Load saved records
load_data()
update_student_list()
refresh_table()

root.mainloop()