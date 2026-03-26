#Populate Database with Test Data
import sqlite3

#Insert Admin (James)
def insert_admin():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    #Check if admin already exists
    cursor.execute("SELECT * FROM admin WHERE username = ?", ("james_admin",))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO admin (username, password) VALUES (?, ?)",
            ("james_admin", "admin123")
        )
        print("Admin inserted successfully")
    else:
        print("Admin already exists")

    conn.commit()
    conn.close()


#Insert Client
def insert_client():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    #Check if client already exists
    cursor.execute("SELECT * FROM clients WHERE name = ?", ("ABC Company",))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO clients (name) VALUES (?)",
            ("ABC Company",)
        )
        print("Client inserted successfully")
    else:
        print("Client already exists")

    conn.commit()
    conn.close()


#Insert Employees
def insert_employees():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    #Get client ID
    cursor.execute("SELECT id FROM clients WHERE name = ?", ("ABC Company",))
    client = cursor.fetchone()
    if client is None:
        print("Client not found. Run insert_client() first.")
        conn.close()
        return
    client_id = client[0]

    #Employee data: (name, username, password, client_id)
    employees = [
        ("Mike", "mike_123", "secure1", client_id),
        ("Anele", "anele_123", "secure2", client_id)
    ]

    for name, username, password, cid in employees:
        cursor.execute("SELECT * FROM employees WHERE username = ?", (username,))
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO employees (name, username, password, client_id) VALUES (?, ?, ?, ?)",
                (name, username, password, cid)
            )
            print(f"Employee {name} inserted successfully")
        else:
            print(f"Employee {name} already exists")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_admin()
    insert_client()
    insert_employees()
    print("Test data population completed")
