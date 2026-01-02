import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import os

class Employee:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("1200x600")

        # ===== Variables =====
        self.eid = tk.IntVar()
        self.ename = tk.StringVar()
        self.edesi = tk.StringVar()
        self.esal = tk.IntVar()
        self.egen = tk.StringVar()
        self.search_txt = tk.StringVar()
        self.search_by = tk.StringVar()

        # ===== Title =====
        title = tk.Label(
            root,
            text="Employee Management System",
            font=("Arial", 30, "bold"),
            bg="white",
            fg="black",
            relief="groove",
            bd=5
        )
        title.pack(side=tk.TOP, fill=tk.X)

        # ===== Frame 1 (Form) =====
        frame1 = tk.Frame(root, bd=5, relief="ridge", bg="red")
        frame1.place(x=10, y=80, width=350, height=500)

        tk.Label(frame1, text="Employee ID", bg="red", fg="white", font=("Arial", 12)).grid(row=0, column=0, pady=10)
        tk.Entry(frame1, textvariable=self.eid).grid(row=0, column=1)

        tk.Label(frame1, text="Name", bg="red", fg="white", font=("Arial", 12)).grid(row=1, column=0, pady=10)
        tk.Entry(frame1, textvariable=self.ename).grid(row=1, column=1)

        tk.Label(frame1, text="Designation", bg="red", fg="white", font=("Arial", 12)).grid(row=2, column=0, pady=10)
        tk.Entry(frame1, textvariable=self.edesi).grid(row=2, column=1)

        tk.Label(frame1, text="Salary", bg="red", fg="white", font=("Arial", 12)).grid(row=3, column=0, pady=10)
        tk.Entry(frame1, textvariable=self.esal).grid(row=3, column=1)

        tk.Label(frame1, text="Gender", bg="red", fg="white", font=("Arial", 12)).grid(row=4, column=0, pady=10)
        ttk.Combobox(frame1, values=("Male", "Female"), textvariable=self.egen, state="readonly").grid(row=4, column=1)

        tk.Label(frame1, text="Address", bg="red", fg="white", font=("Arial", 12)).grid(row=5, column=0, pady=10)
        self.addr = tk.Text(frame1, width=20, height=3)
        self.addr.grid(row=5, column=1)

        # ===== Buttons =====
        tk.Button(frame1, text="Add", command=self.add).grid(row=6, column=0, pady=20)
        tk.Button(frame1, text="Update", command=self.update).grid(row=6, column=1)
        tk.Button(frame1, text="Delete", command=self.delete).grid(row=7, column=0)
        tk.Button(frame1, text="Clear", command=self.clear).grid(row=7, column=1)

        # ===== Frame 2 (Table + Search) =====` `
        frame2 = tk.Frame(root, bd=5, relief="ridge", bg="red")
        frame2.place(x=370, y=80, width=820, height=500)

        ttk.Combobox(frame2, values=("ID", "Name"), textvariable=self.search_by, state="readonly").grid(row=0, column=0, padx=10)
        tk.Entry(frame2, textvariable=self.search_txt).grid(row=0, column=1)
        tk.Button(frame2, text="Search", command=self.search).grid(row=0, column=2)
        tk.Button(frame2, text="Show All", command=self.fetch).grid(row=0, column=3)

        # ===== Table =====
        self.table = ttk.Treeview(
            frame2,
            columns=("ID", "Name", "Designation", "Salary", "Gender", "Address"),
            show="headings"
        )

        for col in ("ID", "Name", "Designation", "Salary", "Gender", "Address"):
            self.table.heading(col, text=col)
            self.table.column(col, width=120)

        self.table.grid(row=1, column=0, columnspan=4, pady=20)
        self.table.bind("<ButtonRelease-1>", self.fill_form)

        self.fetch()

    # ===== Database Connection =====
  



    def connect(self):
        return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )


    # ===== Add =====
    def add(self):
        con = self.connect()
        cur = con.cursor()

        cur.execute(
            "INSERT INTO emp VALUES (%s,%s,%s,%s,%s)",
            (self.eid.get(), self.ename.get(), self.edesi.get(), self.egen.get(), self.addr.get("1.0", tk.END))
        )

        cur.execute(
            "INSERT INTO salary VALUES (%s,%s)",
            (self.eid.get(), self.esal.get())
        )

        con.commit()
        con.close()
        messagebox.showinfo("Success", "Employee Added")
        self.fetch()

    # ===== Fetch =====
    def fetch(self):
        con = self.connect()
        cur = con.cursor()

        cur.execute("""
            SELECT e.id, e.name, e.designation, s.salary, e.gender, e.address
            FROM emp e JOIN salary s ON e.id = s.emp_id
        """)

        rows = cur.fetchall()
        self.table.delete(*self.table.get_children())
        for row in rows:
            self.table.insert("", tk.END, values=row)

        con.close()

    # ===== Fill Form =====
    def fill_form(self):
        row = self.table.item(self.table.focus())["values"]
        if row:
            self.eid.set(row[0])
            self.ename.set(row[1])
            self.edesi.set(row[2])
            self.esal.set(row[3])
            self.egen.set(row[4])
            self.addr.delete("1.0", tk.END)
            self.addr.insert(tk.END, row[5])

    # ===== Update =====
    def update(self):
        con = self.connect()
        cur = con.cursor()

        cur.execute(
            "UPDATE emp SET name=%s, designation=%s, gender=%s, address=%s WHERE id=%s",
            (self.ename.get(), self.edesi.get(), self.egen.get(), self.addr.get("1.0", tk.END), self.eid.get())
        )

        cur.execute(
            "UPDATE salary SET salary=%s WHERE emp_id=%s",
            (self.esal.get(), self.eid.get())
        )

        con.commit()
        con.close()
        messagebox.showinfo("Success", "Updated Successfully")
        self.fetch()

    # ===== Delete =====
    def delete(self):
        con = self.connect()
        cur = con.cursor()
        cur.execute("DELETE FROM emp WHERE id=%s", self.eid.get())
        con.commit()
        con.close()
        messagebox.showinfo("Success", "Deleted Successfully")
        self.fetch()

    # ===== Search =====
    def search(self):
        con = self.connect()
        cur = con.cursor()

        if self.search_by.get() == "ID":
            cur.execute("""
                SELECT e.id, e.name, e.designation, s.salary, e.gender, e.address
                FROM emp e JOIN salary s ON e.id = s.emp_id
                WHERE e.id=%s
            """, self.search_txt.get())
        else:
            cur.execute("""
                SELECT e.id, e.name, e.designation, s.salary, e.gender, e.address
                FROM emp e JOIN salary s ON e.id = s.emp_id
                WHERE e.name LIKE %s
            """, ("%"+self.search_txt.get()+"%",))

        rows = cur.fetchall()
        self.table.delete(*self.table.get_children())
        for row in rows:
            self.table.insert("", tk.END, values=row)

        con.close()

    # ===== Clear =====
    def clear(self):
        self.eid.set("")
        self.ename.set("")
        self.edesi.set("")
        self.esal.set("")
        self.egen.set("")
        self.addr.delete("1.0", tk.END)


root = tk.Tk()
app = Employee(root)
root.mainloop()
