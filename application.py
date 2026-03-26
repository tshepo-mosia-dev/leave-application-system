#This is a code for a program that checks or/and apply for work leave.
#Also covers the logic of James (Admin) reviewing applications

import sqlite3
from datetime import datetime #This module will provide us with class to work with date and time for when we calculate leave days

database = "database.db"

def connect_db():
    return sqlite3.connect(database)

#Login function
def employee_login():
    conn = connect_db()
    cursor = conn.cursor()
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    cursor.execute("SELECT id, name, leave_balance FROM employees WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()

    if result:
        employee_id, name, leave_balance = result
        print("\nWelcome " + name + ". Your current leave balance is " + str(leave_balance) + " days.\n")
        employee_menu(employee_id)
    else:
        print("Invalid credentials. Try again.\n")
        employee_login()

def employee_menu(employee_id):
    while True:
        print("1. Check Leave Balance")
        print("2. Apply for Leave")
        print("3. Logout")
        choice = input("Select an option: ")

        if choice == "1":
            check_leave_balance(employee_id)
        elif choice == "2":
            apply_leave(employee_id)
        elif choice == "3":
            print("Logging out...\n")
            break
        else:
            print("Invalid choice. Try again.\n")
            employee_menu(employee_id)

def check_leave_balance(employee_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT leave_balance FROM employees WHERE id=?", (employee_id,))
    leave_balance = cursor.fetchone()[0]
    conn.close()
    print("Your current leave balance is " + str(leave_balance) + " days.\n")

def apply_leave(employee_id):
    start_date = input("Enter leave start date (YYYY-MM-DD): ")
    end_date = input("Enter leave end date (YYYY-MM-DD): ")

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        days_requested = (end - start).days + 1
        if days_requested <= 0:
            print("End date must be after start date.\n")
            return
    except ValueError:
        print("Invalid date format.\n")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT leave_balance FROM employees WHERE id=?", (employee_id,))
    leave_balance = cursor.fetchone()[0]

    if days_requested > leave_balance:
        print("Requested leave days are higher than available days. You only have " + str(leave_balance) + " days remaining.\n")
    else:
        cursor.execute("INSERT INTO apply_leave (employee_id, start_date, end_date) VALUES (?, ?, ?)",
                    (employee_id, start_date, end_date))
        #Deduct leave immediately (can also deduct after approval)
        cursor.execute("UPDATE employees SET leave_balance = leave_balance - ? WHERE id=?", (days_requested, employee_id))
        conn.commit()
        print("Leave applied for " + str(days_requested) + " days. Pending approval.\n")
    conn.close()

#Admin (James) Functions
def admin_login():
    conn = connect_db()
    cursor = conn.cursor()
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    cursor.execute("SELECT id FROM admin WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()

    if result:
        print("\nWelcome Admin\n")
        admin_menu()
    else:
        print("Invalid admin credentials. Try again.\n")
        admin_login()

def admin_menu():
    while True:
        print("1. View Leave Applications")
        print("2. Approve/Reject Leave")
        print("3. Logout")
        choice = input("Select an option: ")

        if choice == "1":
            view_applications()
        elif choice == "2":
            review_leave_application()
        elif choice == "3":
            print("Logging out...\n")
            break
        else:
            print("Invalid choice. Try again.\n")

def view_applications():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT apply_leave.id, employees.name, start_date, end_date, status
        FROM apply_leave
        JOIN employees ON apply_leave.employee_id = employees.id
    """)
    applications = cursor.fetchall()
    conn.close()

    if applications:
        print("\nLeave Applications:")
        for app in applications:
            print("ID: " + str(app[0]) + ", Employee: " + app[1] + ", From: " + app[2] + ", To: " + app[3] + ", Status: " + app[4] + ".")
        print("")
    else:
        print("\nℹ No leave applications found.\n")

def review_leave_application():
    view_applications()
    app_id = input("Enter Application ID to review: ")

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT employee_id, start_date, end_date, status FROM apply_leave WHERE id=?", (app_id,))
    app = cur.fetchone()

    if not app:
        print("Application not found.\n")
        conn.close()
        return

    employee_id, start_date, end_date, status = app
    if status != "pending":
        print("This application is already " + status)
        conn.close()
        return

    decision = input("Approve? (Y/N): ").strip().upper()
    if decision == "Y":
        cur.execute("UPDATE apply_leave SET status='approved' WHERE id=?", (app_id,))
        conn.commit()
        print("Leave approved.\n")
    elif decision == "N":
        #Restore leave balance if previously deducted
        days_requested = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days + 1
        cur.execute("UPDATE apply_leave SET status='rejected' WHERE id=?", (app_id,))
        cur.execute("UPDATE employees SET leave_balance = leave_balance + ? WHERE id=?", (days_requested, employee_id))
        conn.commit()
        print("Leave rejected. Balance restored.\n")
    else:
        print("Invalid choice.\n")

    conn.close()

#Main Menu
def main_menu():
    while True:
        print("Leave Management System")
        print("1. Employee Login")
        print("2. Admin Login")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            employee_login()
        elif choice == "2":
            admin_login()
        elif choice == "3":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    main_menu()