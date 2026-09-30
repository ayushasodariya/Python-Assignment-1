# Programming with Python - Assignment 1

## Student Details

- **Name:** Ayush Asodariya
- **Enrollment No.:** 12502080603002
- **Course:** Programming with Python
- **Course Code:** 202044504
- **Semester:** 5th Semester
- **Branch:** Information Technology

---

## Questions Included

| Question | Topic |
|---|---|
| Q1 | Campus Merit Analyzer |
| Q2 | Optimized Password Audit |
| Q3 | Recursive Expression Engine |
| Q4 | CSV Transaction Splitter |
| Q5 | Bank Settlement System |
| Q6 | Module Dependency Resolver |
| Q7 | Interactive Formula Validator |
| Q8 | Compressed Log Index |
| Q9 | Threaded Job Scheduler |
| Q10 | Tkinter Assignment Tracker |

---

## Folder Structure

```text
Assignment 1
│
├── README.md
│
├── 12502080603002_Assignment1_Q1.py
├── 12502080603002_Assignment1_Q2.py
├── 12502080603002_Assignment1_Q3.py
├── 12502080603002_Assignment1_Q4/
├── 12502080603002_Assignment1_Q5.py
├── 12502080603002_Assignment1_Q6.py
├── 12502080603002_Assignment1_Q7.py
├── 12502080603002_Assignment1_Q8/
├── 12502080603002_Assignment1_Q9.py
└── 12502080603002_Assignment1_Q10/
```

Q4, Q8 and Q10 have been kept as folders because they need supporting files.

---

# What each question does

### Q1 - Campus Merit Analyzer

This program stores student information and finds the top students semester-wise.

It uses CPI as the main factor. If CPI is the same, average marks are checked, and if those are also the same, the enrollment number is used.

It also finds the topper for each subject.

**Main topics:** lists, tuples, dictionaries and sorting.

---

### Q2 - Password Audit

This program checks whether a password is strong or not.

It checks things like:

- Password length
- Lowercase letter
- Uppercase letter
- Number
- Special character
- Banned words
- Repeated characters

The result can be `STRONG`, `WEAK_LENGTH`, `WEAK_PATTERN` or `COMPROMISED`.

**Main topics:** strings, regular expressions and validation.

---

### Q3 - Recursive Expression Engine

This program evaluates expressions containing numbers, variables, `+`, `-`, `*` and brackets.

Variables can depend on other variables, so the program evaluates them when required.

It also checks for circular dependencies and invalid expressions.

**Main topics:** recursion, parsing, dictionaries, memoization and cycle detection.

---

### Q4 - CSV Transaction Splitter

This program reads transactions from a CSV file.

Valid credit and debit transactions are separated into different files. Invalid rows are put into `error.csv` with the reason why they were rejected.

The program also shows the net balance change for each account.

**Main topics:** CSV, file handling, dictionaries and exception handling.

---

### Q5 - Bank Settlement System

This is an OOP-based bank program.

It supports:

- Deposit
- Withdraw
- Transfer
- Transaction history
- Batch operations
- Rollback when a batch fails

Custom exceptions are used for banking errors such as insufficient balance.

**Main topics:** classes, objects, OOP, custom exceptions and rollback.

---

### Q6 - Module Dependency Resolver

This program treats modules and their imports as a graph.

It finds a valid order in which the modules can be loaded. Duplicate dependencies are ignored.

If the modules contain a circular dependency, the program reports a cycle.

**Main topics:** graphs, topological sorting, heaps and cycle detection.

---

### Q7 - Formula Validator

This is an interactive calculator.

It supports:

```text
+
-
*
/
%
```

Variables can also be stored, for example:

```text
x = 10
x + 5
```

The program keeps running until `quit` is entered.

Different errors are handled using separate custom exceptions.

**Main topics:** exception handling, dictionaries and parsing.

---

### Q8 - Compressed Log Index

This program works with server log files.

In BUILD mode it reads the log files, creates an index of words and their locations, saves the index using pickle and creates a ZIP archive.

In SEARCH mode it loads the index and searches for words.

The `logs` folder contains the test log files used for this question.

**Main topics:** file handling, text processing, dictionaries, pickle and ZIP files.

---

### Q9 - Threaded Job Scheduler

This program simulates a job scheduler with multiple workers.

Jobs have an arrival time, priority and duration. Higher priority jobs are selected first and jobs with the same priority are handled according to arrival order.

The program shows which worker handled each job and calculates average waiting time.

**Main topics:** threading, priority queues, heaps and scheduling.

---

### Q10 - Tkinter Assignment Tracker

This is a small GUI application for keeping track of student assignments.

It can:

- Add students
- Add assignment submissions
- Update marks
- Set Pending/Completed status
- Filter submissions
- Export a CSV report
- Save data locally

The saved data is kept in `assignment_data.json`.

**Main topics:** Tkinter, GUI programming, JSON, CSV and validation.

---

# Requirements

I used **Python 3.10 or above**.

To check your Python version:

```bash
python --version
```

No extra Python packages are needed for these programs.

Q10 uses Tkinter, which normally comes with Python on Windows.

---

# How to Run

Open PowerShell or Command Prompt in the folder of the question you want to run.

For example:

```bash
python 12502080603002_Assignment1_Q1.py
```

For Q5:

```bash
python 12502080603002_Assignment1_Q5.py
```

For Q10:

```bash
python 12502080603002_Assignment1_Q10.py
```

Some questions have supporting files, so keep those files in their original folders.

---

# Testing

I tested the programs with the sample inputs as well as some additional inputs.

I also checked some invalid and boundary cases, such as:

- Invalid marks
- Empty input
- Duplicate student
- Invalid transaction amount
- Division by zero
- Unknown variables
- Circular dependencies
- Passwords with repeated characters
- Pending and completed submissions
- Saving and loading Q10 data

---

# Files Generated During Testing

Some programs create files while running.

For example:

```text
credit.csv
debit.csv
error.csv
assignment_data.json
```

---

# Things I Practiced

Through these questions I worked with:

- Lists and tuples
- Dictionaries
- Functions
- Sorting
- Regular expressions
- Recursion
- Memoization
- Exception handling
- CSV files
- JSON files
- Object-oriented programming
- Graphs
- Heaps and priority queues
- Multithreading
- Tkinter GUI

---


This repository contains the source code and supporting files for my Programming with Python Assignment 1
