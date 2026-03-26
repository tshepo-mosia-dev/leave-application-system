import customtkinter as ctk
from tkinter import messagebox
import application  #this imports your backend logic (application.py)

#Setup main window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LeaveApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Leave Management System")
        self.geometry("400x400")

        self.current_user_id = None
        self.current_role = None

        self.login_page()

    #Login page
    def login_page(self):
        for widget in self.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(self, text="Leave Management System", font=("Arial", 20, "bold"))
        title.pack(pady=20)

        self.role_var = ctk.StringVar(value="Employee")
        #User dropdown fuction setup
        ctk.CTkLabel(self, text="Select Role").pack()
        role_dropdown = ctk.CTkOptionMenu(self, values=["Employee", "Admin"], variable=self.role_var)
        role_dropdown.pack(pady=5)
        
        #Username and Password fields setup
        ctk.CTkLabel(self, text="Username").pack(anchor="w", padx=60, pady=(20, 0))
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(anchor="w", padx=60, pady=(0, 10))

        ctk.CTkLabel(self, text="Password").pack(anchor="w", padx=60, pady=(5, 0))
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(anchor="w", padx=60, pady=(0, 10))

        login_btn = ctk.CTkButton(self, text="Login", command=self.handle_login)
        login_btn.pack(anchor="w", padx=60, pady=15)

    #API part that gets the user login credentials    
    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()

        if not username or not password: #If either username or password is incorrect, error message will pop up
            messagebox.showwarning("Input Error", "Please enter correct username and password.")
            return
        
        conn = application.connect_db()
        cur = conn.cursor()

        if role == "Employee":
            cur.execute("SELECT id, name, leave_balance FROM employees WHERE username=? AND password=?", (username, password))
        else:
            cur.execute("SELECT id FROM admin WHERE username=? AND password=?", (username, password))

        result = cur.fetchone()
        conn.close()

        if result:
            if role == "Employee":
                self.current_user_id, name, balance = result
                self.current_role = "Employee"
                self.create_employee_dashboard(name, balance)
            else:
                self.current_role = "Admin"
                self.create_admin_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials. Try again.")

    #Employee Dashboard
    def create_employee_dashboard(self, name, balance):
        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self, text=f"Welcome, {name}", font=("Arial", 18, "bold")).pack(pady=10)
        self.balance_label = ctk.CTkLabel(self, text=f"Leave Balance: {balance} days")
        self.balance_label.pack(pady=5)

        ctk.CTkButton(self, text="Apply for Leave", command=self.open_leave_window).pack(pady=10)
        ctk.CTkButton(self, text="Check Leave Balance", command=self.update_leave_balance).pack(pady=10)
        ctk.CTkButton(self, text="Logout", fg_color="red", command=self.login_page).pack(pady=20)

    #Leave Application Window setup
    def open_leave_window(self):
        leave_window = ctk.CTkToplevel(self)
        leave_window.title("Apply for Leave")
        leave_window.geometry("300x250")

        ctk.CTkLabel(leave_window, text="Start Date (YYYY-MM-DD)").pack(pady=5)
        start_entry = ctk.CTkEntry(leave_window)
        start_entry.pack()

        ctk.CTkLabel(leave_window, text="End Date (YYYY-MM-DD)").pack(pady=5)
        end_entry = ctk.CTkEntry(leave_window)
        end_entry.pack()

        def apply():
            start_date = start_entry.get().strip()
            end_date = end_entry.get().strip()

            conn = application.connect_db()
            cur = conn.cursor()
            cur.execute("SELECT leave_balance FROM employees WHERE id=?", (self.current_user_id,))
            balance = cur.fetchone()[0]
            conn.close()

            from datetime import datetime
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.strptime(end_date, "%Y-%m-%d")
                days_requested = (end - start).days + 1

                if days_requested <= 0:
                    messagebox.showerror("Error", "End date must be after start date.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Invalid date format.")
                return
            
            if days_requested > balance:
                messagebox.showerror("Error", f"You only have {balance} days remaining.")
                return
            
            conn = application.connect_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO apply_leave (employee_id, start_date, end_date) VALUES (?, ?, ?)",
                        (self.current_user_id, start_date, end_date))
            cur.execute("UPDATE employees SET leave_balance = leave_balance - ? WHERE id=?",
                        (days_requested, self.current_user_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"Leave applied for {days_requested} days.")
            leave_window.destroy()
            self.update_leave_balance()

        ctk.CTkButton(leave_window, text="Submit", command=apply).pack(pady=15)

    def update_leave_balance(self):
        conn = application.connect_db()
        cur = conn.cursor()
        cur.execute("SELECT leave_balance FROM employees WHERE id=?", (self.current_user_id,))
        new_balance = cur.fetchone()[0]
        conn.close()

        self.balance_label.configure(text=f"Leave Balance: {new_balance} days")
        messagebox.showinfo("Leave Days", f"Updated available leave days: {new_balance}.")

    #ADMIN DASHBOARD
    def create_admin_dashboard(self):
        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self, text="Admin Dashboard", font=("Arial", 18, "bold")).pack(pady=10)
        ctk.CTkButton(self, text="View Applications", command=self.view_applications).pack(pady=10)
        ctk.CTkButton(self, text="Logout", fg_color="red", command=self.login_page).pack(pady=20)

    def view_applications(self):
        conn = application.connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT apply_leave.id, employees.name, start_date, end_date, status
            FROM apply_leave
            JOIN employees ON apply_leave.employee_id = employees.id
        """)
        applications = cur.fetchall()
        conn.close()

        view_window = ctk.CTkToplevel(self)
        view_window.title("Leave Applications")
        view_window.geometry("500x400")

        if not applications:
            ctk.CTkLabel(view_window, text="No applications found.").pack(pady=10)
            return
        
        for app in applications:
            app_id, emp_name, start, end, status = app
            frame = ctk.CTkFrame(view_window)
            frame.pack(fill="x", pady=5, padx=10)

            ctk.CTkLabel(frame, text=f"{emp_name} | {start} → {end} | Status: {status}").pack(side="left", padx=5)

            if status == "pending":
                approve_btn = ctk.CTkButton(frame, text="Approve", width=60, fg_color="green",
                                            command=lambda i=app_id: self.update_status(i, "approved", view_window))
                reject_btn = ctk.CTkButton(frame, text="Reject", width=60, fg_color="red",
                                           command=lambda i=app_id: self.update_status(i, "rejected", view_window))
                approve_btn.pack(side="left", padx=5)
                reject_btn.pack(side="left", padx=5)

    def update_status(self, app_id, status, window):
        conn = application.connect_db()
        cur = conn.cursor()

        cur.execute("SELECT employee_id, start_date, end_date FROM apply_leave WHERE id=?", (app_id,))
        emp_id, start, end = cur.fetchone()

        from datetime import datetime
        days_requested = (datetime.strptime(end, "%Y-%m-%d") - datetime.strptime(start, "%Y-%m-%d")).days + 1

        if status == "approved":
            cur.execute("UPDATE apply_leave SET status='approved' WHERE id=?", (app_id,))
        else:
            cur.execute("UPDATE apply_leave SET status='rejected' WHERE id=?", (app_id,))
            cur.execute("UPDATE employees SET leave_balance = leave_balance + ? WHERE id=?", (days_requested, emp_id))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Application {status.capitalize()} successfully!")
        window.destroy()
        self.create_admin_dashboard()

if __name__ == "__main__":
    app = LeaveApp()
    app.mainloop()