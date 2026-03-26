Project Title and Description
Project Title: Leave Application and Monitoring API System
Developer: Group 08

Description:
The Leave Application and Monitoring API System is a three-tier application built using Python. It automates how employees apply for leave and how administrators (like HR consultants) manage those requests. It uses an SQLite database for data storage, an API for communication, and a CustomTkinter GUI for an easy-to-use desktop interface.

Key Functions:
* Employees can log in, check their leave balance, and apply for leave.
* Admins can view, approve, or reject leave requests.
* Automatic leave balance updates after each approval or rejection.
* Works as both a Python app and a standalone `.exe` file.

Installation Instructions:
Option 1: Run the Python Files Directly
1. Ensure Python 3.10+ is installed on your computer.
2. Download or clone the project folder:
a. Leave Application
i. application.py
ii. gui_app.py
iii. database.py
iv. database.db
v. README.txt
3. Open a terminal or command prompt in the project directory.
4. Install dependencies (if required):
a. Install customtkinter
5. Run the GUI application:
a. gui_app.py

Option 2: Use the Executable Version
1. Navigate to the dist folder inside the project.
2. Ensure database.db is in the same folder as the executable file.
3. Double-click Leave Link.exe to launch the application.
4. The program will open a user-friendly interface for login and use.
Available Users:
Admin
* Username: james_admin
* Password: admin123
Employee 1
* Username: mike_123
* Password: secure1
Employee 2
* Username: anele_123
* Password: secure2

Database Overview
You can open database.db using DB Browser for SQLite to view all records:
* employees - stores employee info & leave balances
* admin - stores admin credentials
* apply_leave - stores leave requests

Contribution Ideas:
* Add email or SMS notifications for approved/rejected leave.
* Implement password encryption.
* Create a web version.
*  Add a dashboard for HR analytics.

Licensing Information
This project is licensed under the Group 08 of IFS140 2025.
You are free to:
* Use, copy, and modify this project for personal or educational purposes.
* Share it with proper credit to the author.

Copyright © 2025 Group 08 of IFS140 2025.
Developed for educational purposes under the IFS140 Capstone Project at UWC.
