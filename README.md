# StudentManagementSystemProject

Student Management System (Tkinter + MySQL)

This is a Python-based Student Management System built using Tkinter for the GUI and MySQL for the backend database. It allows users to add, view, update, delete, and search student records.

Features:
- Add Student
- View All Students
- Update Student
- Delete Student
- Search Student
- Auto Database Setup

Technologies Used:
- Python 3.x
- Tkinter
- MySQL
- mysql-connector-python

Requirements:
- Python 3.x
- mysql-connector-python (install via pip)
- MySQL server running locally

How to Run:
1. Install required packages: pip install mysql-connector-python
2. Run the script: python main.py

Database Schema:
Table: students
- roll_number (VARCHAR 50, Primary Key)
- name (VARCHAR 100)
- email (VARCHAR 100)
- phone (VARCHAR 20)
- gender (VARCHAR 10)
- dob (VARCHAR 20)
- address (TEXT)

Error Handling:
- MySQL connection errors are shown in message boxes.
- Duplicate roll numbers are prevented.
- Input validation is included.

Future Enhancements:
- Login authentication
- CSV/Excel export
- Data validation
- Modern UI

Usage:
- Use the GUI to add, update, delete, and search student records.
- Data is stored in MySQL and displayed in a table.
