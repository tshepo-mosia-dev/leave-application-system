#Database setup: creates a leave management database with three related tables
import sqlite3

def create_tables(): #this function named create_tables we will use it to create the database and tables
    db_connection = sqlite3.connect("database.db") #creates database files called database.db
    cursor = db_connection.cursor() #the cursor in sql goes through the database row by row. instead of going through it all at once

    #Creates clients table (companies or businesses James will be assisting)
    cursor.execute('''
                   create table if not exists clients(
                   id integer primary key autoincrement,
                   name text not null)
                   ''')

    #Creates employees table (employees of businesses James will be assisting)
    cursor.execute('''
                   create table if not exists employees(
                   id integer primary key autoincrement,
                   name text not null,
                   username text unique not null,
                   password text not null,
                   client_id integer,
                   leave_balance integer default 21,
                   FOREIGN key (client_id) references clients(id))
                   ''')

    #Creates leave application table
    cursor.execute('''
                   create table if not exists apply_leave(
                   id integer primary key autoincrement,
                   employee_id integer,
                   start_date text,
                   end_date text,
                   status test default 'pending',
                   FOREIGN key (employee_id) references employees(id))
                   ''')
    
    #Creates admin table (THis is for James)
    cursor.execute('''
                   create table if not exists admin(
                   id integer primary key autoincrement,
                   username text unique not null,
                   password text not null)
                   ''')

    db_connection.commit() #this makes sure we save all changes made, without it (commit()) changes might not be written to database file
    db_connection.close() #this closes the connection to the database

if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully!")