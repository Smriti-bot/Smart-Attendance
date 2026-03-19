import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import pandas as pd
import cv2

from app.recognizer import start_attendance
from app.encoder import encode_faces
from app.database import init_db, create_default_admin


def launch_gui():

    # Initialize database
    init_db()
    create_default_admin()

    # ================= DASHBOARD FUNCTION =================

    def open_dashboard():

        root = tk.Tk()
        root.title("Smart Attendance System")
        root.geometry("600x550")
        root.configure(bg="#1e1e1e")

        tk.Label(root,
                 text="Smart Attendance System",
                 font=("Arial", 20, "bold"),
                 bg="#1e1e1e",
                 fg="white").pack(pady=20)

        # ---------- Student Registration ----------

        def register_student():

            reg_window = tk.Toplevel(root)
            reg_window.title("Register Student")
            reg_window.geometry("400x250")

            tk.Label(reg_window, text="Enter Student Name").pack(pady=10)

            name_entry = tk.Entry(reg_window)
            name_entry.pack(pady=10)

            def capture_face():

                name = name_entry.get()

                if not name:
                    messagebox.showerror("Error", "Please enter name")
                    return

                cap = cv2.VideoCapture(0)

                while True:
                    ret, frame = cap.read()
                    cv2.imshow("Press SPACE to Capture", frame)

                    if cv2.waitKey(1) & 0xFF == 32:  # SPACE key
                        cv2.imwrite(f"data/dataSet/{name}.jpg", frame)
                        break

                cap.release()
                cv2.destroyAllWindows()

                encode_faces()
                messagebox.showinfo("Success",
                                    "Student Registered & Trained Successfully")
                reg_window.destroy()

            tk.Button(reg_window,
                      text="Capture Face",
                      command=capture_face).pack(pady=20)

        # ---------- Other Functions ----------

        def train_faces():
            encode_faces()
            messagebox.showinfo("Success", "Face database rebuilt!")

        def view_attendance():

            view_window = tk.Toplevel(root)
            view_window.title("Attendance Records")
            view_window.geometry("700x400")

            tree = ttk.Treeview(view_window)
            tree["columns"] = ("ID", "Name", "Date", "Time")

            tree.column("#0", width=0, stretch=tk.NO)
            tree.column("ID", anchor=tk.CENTER, width=50)
            tree.column("Name", anchor=tk.CENTER, width=200)
            tree.column("Date", anchor=tk.CENTER, width=150)
            tree.column("Time", anchor=tk.CENTER, width=150)

            tree.heading("ID", text="ID")
            tree.heading("Name", text="Name")
            tree.heading("Date", text="Date")
            tree.heading("Time", text="Time")

            conn = sqlite3.connect("data/attendance.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM attendance")

            for row in cursor.fetchall():
                tree.insert("", "end", values=row)

            conn.close()
            tree.pack(fill="both", expand=True)

        def export_excel():
            conn = sqlite3.connect("data/attendance.db")
            df = pd.read_sql_query("SELECT * FROM attendance", conn)
            df.to_excel("reports/attendance_report.xlsx", index=False)
            conn.close()
            messagebox.showinfo("Exported",
                                "Report saved in reports folder.")

        # ---------- Buttons ----------

        tk.Button(root,
                  text="Register New Student",
                  width=35,
                  height=2,
                  bg="#00BCD4",
                  fg="white",
                  command=register_student).pack(pady=10)

        tk.Button(root,
                  text="Train / Rebuild Face Database",
                  width=35,
                  height=2,
                  bg="#4CAF50",
                  fg="white",
                  command=train_faces).pack(pady=10)

        tk.Button(root,
                  text="Start Attendance",
                  width=35,
                  height=2,
                  bg="#2196F3",
                  fg="white",
                  command=start_attendance).pack(pady=10)

        tk.Button(root,
                  text="View Attendance Records",
                  width=35,
                  height=2,
                  bg="#FF9800",
                  fg="white",
                  command=view_attendance).pack(pady=10)

        tk.Button(root,
                  text="Export to Excel",
                  width=35,
                  height=2,
                  bg="#9C27B0",
                  fg="white",
                  command=export_excel).pack(pady=10)

        root.mainloop()

    # ================= LOGIN WINDOW =================

    login = tk.Tk()
    login.title("Admin Login")
    login.geometry("400x300")
    login.configure(bg="#1e1e1e")

    tk.Label(login,
             text="Admin Login",
             font=("Arial", 18, "bold"),
             bg="#1e1e1e",
             fg="white").pack(pady=20)

    tk.Label(login, text="Username",
             bg="#1e1e1e",
             fg="white").pack()

    entry_user = tk.Entry(login)
    entry_user.pack(pady=5)

    tk.Label(login, text="Password",
             bg="#1e1e1e",
             fg="white").pack()

    entry_pass = tk.Entry(login, show="*")
    entry_pass.pack(pady=5)

    def authenticate():
        username = entry_user.get()
        password = entry_pass.get()

        conn = sqlite3.connect("data/attendance.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM admin WHERE username=? AND password=?",
            (username, password)
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            login.destroy()
            open_dashboard()
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    tk.Button(login,
              text="Login",
              command=authenticate,
              bg="#4CAF50",
              fg="white",
              width=15).pack(pady=20)

    login.mainloop()
    