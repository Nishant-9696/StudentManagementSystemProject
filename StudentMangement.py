
import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector 


MYSQL_CONFIG = {
    'user': 'root',     
    'password': 'Nishant',  
    'host': 'localhost',
    'database': 'student_management_system' 
}


class StudentDB:
    def __init__(self, config=MYSQL_CONFIG):
        self.config = config
        self.con = None
        self.cur = None
        self.create_database_and_table()

    def connect(self):
        try:
            self.con = mysql.connector.connect(**self.config)
            self.cur = self.con.cursor()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Connection Error", 
                                 f"Failed to connect to MySQL: {err}\n"
                                 "Please check your connection settings (user, password, host, database) "
                                 "and ensure MySQL server is running.")
            self.con = None
            self.cur = None
            return False

    def disconnect(self):
        if self.con and self.con.is_connected():
            self.con.close()
            self.con = None
            self.cur = None

    def create_database_and_table(self):
        temp_config = {k: v for k, v in self.config.items() if k != 'database'}
        db_name = self.config['database']
        
        try:
            temp_con = mysql.connector.connect(**temp_config)
            temp_cur = temp_con.cursor()
            
            temp_cur.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            temp_con.commit()
            temp_cur.close()
            temp_con.close()
            
            if self.connect():
                self.cur.execute("""
                    CREATE TABLE IF NOT EXISTS students (
                        roll_number VARCHAR(50) PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(100),
                        phone VARCHAR(20),
                        gender VARCHAR(10),
                        dob VARCHAR(20),
                        address TEXT
                    )
                """)
                self.con.commit()
            
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error setting up database/table: {e}")
        finally:
            self.disconnect()

    def add_student(self, roll, name, email, phone, gender, dob, address):
        if not self.connect(): return False
        try:
            query = """
                INSERT INTO students (roll_number, name, email, phone, gender, dob, address) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            self.cur.execute(query, (roll, name, email, phone, gender, dob, address))
            self.con.commit()
            return True
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Roll Number already exists!")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to Add Record: {e}")
            return False
        finally:
            self.disconnect()

    def fetch_students(self, search_key=None, search_value=None):
        if not self.connect(): return []
        try:
            if search_key and search_value:
                query = f"SELECT * FROM students WHERE {search_key} LIKE %s"
                self.cur.execute(query, ('%' + search_value + '%',))
            else:
                self.cur.execute("SELECT * FROM students")
            
            rows = self.cur.fetchall()
            return rows
        except Exception as e:
            messagebox.showerror("Error", f"Failed to Fetch Records: {e}")
            return []
        finally:
            self.disconnect()

    def update_student(self, roll, name, email, phone, gender, dob, address):
        if not self.connect(): return False
        try:
            query = """
                UPDATE students SET name=%s, email=%s, phone=%s, gender=%s, dob=%s, address=%s
                WHERE roll_number=%s
            """
            self.cur.execute(query, (name, email, phone, gender, dob, address, roll))
            self.con.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to Update Record: {e}")
            return False
        finally:
            self.disconnect()

    def delete_student(self, roll):
        if not self.connect(): return False
        try:
            self.cur.execute("DELETE FROM students WHERE roll_number=%s", (roll,))
            self.con.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to Delete Record: {e}")
            return False
        finally:
            self.disconnect()


class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1350x700+0+0")
        
        self.db = StudentDB()

        self.roll_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.gender_var = tk.StringVar(value='Male') 
        self.dob_var = tk.StringVar()
        self.search_by_var = tk.StringVar(value='name') 
        self.search_txt_var = tk.StringVar()
        
        lbl_title = tk.Label(self.root, text="STUDENT MANAGEMENT SYSTEM", 
                             bd=4, relief=tk.GROOVE, font=("times new roman", 40, "bold"), bg="blue", fg="white")
        lbl_title.pack(side=tk.TOP, fill=tk.X)
        
        self.design_gui()
        
        self.display_data()

    def design_gui(self):

        Manage_Frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE, bg="light blue")
        Manage_Frame.place(x=20, y=100, width=450, height=580)
        
        m_title = tk.Label(Manage_Frame, text="Manage Students", bg="light blue", fg="black", font=("times new roman", 20, "bold"))
        m_title.grid(row=0, columnspan=2, pady=20)
        
        fields = [
            ("Roll No.", self.roll_var), ("Name", self.name_var), 
            ("Email", self.email_var), ("Contact", self.phone_var),
            ("DOB (YYYY-MM-DD)", self.dob_var)
        ]
        
        row_num = 1
        for text, var in fields:
            lbl = tk.Label(Manage_Frame, text=text + ":", bg="light blue", fg="black", font=("times new roman", 15, "bold"))
            lbl.grid(row=row_num, column=0, pady=10, padx=20, sticky="w")
            
            txt = tk.Entry(Manage_Frame, textvariable=var, font=("times new roman", 15), bd=2, relief=tk.GROOVE)
            txt.grid(row=row_num, column=1, pady=10, padx=20, sticky="w")
            row_num += 1

        lbl_gender = tk.Label(Manage_Frame, text="Gender:", bg="light blue", fg="black", font=("times new roman", 15, "bold"))
        lbl_gender.grid(row=row_num, column=0, pady=10, padx=20, sticky="w")
        self.gender_combo = ttk.Combobox(Manage_Frame, textvariable=self.gender_var, font=("times new roman", 13), state='readonly')
        self.gender_combo['values'] = ('Male', 'Female', 'Other')
        self.gender_combo.grid(row=row_num, column=1, pady=10, padx=20, sticky="w")
        row_num += 1

        lbl_address = tk.Label(Manage_Frame, text="Address:", bg="light blue", fg="black", font=("times new roman", 15, "bold"))
        lbl_address.grid(row=row_num, column=0, pady=10, padx=20, sticky="w")
        self.address_txt = tk.Text(Manage_Frame, width=20, height=4, font=("times new roman", 13), bd=2, relief=tk.GROOVE)
        self.address_txt.grid(row=row_num, column=1, pady=10, padx=20, sticky="w")
        
        btn_frame = tk.Frame(Manage_Frame, bd=4, relief=tk.RIDGE, bg="light blue")
        btn_frame.place(x=10, y=520, width=420, height=50)

        add_btn = tk.Button(btn_frame, text="Add", width=10, command=self.add_student)
        add_btn.grid(row=0, column=0, padx=5, pady=5)
        
        update_btn = tk.Button(btn_frame, text="Update", width=10, command=self.update_student)
        update_btn.grid(row=0, column=1, padx=5, pady=5)
        
        delete_btn = tk.Button(btn_frame, text="Delete", width=10, command=self.delete_student)
        delete_btn.grid(row=0, column=2, padx=5, pady=5)
        
        clear_btn = tk.Button(btn_frame, text="Clear", width=10, command=self.clear_fields)
        clear_btn.grid(row=0, column=3, padx=5, pady=5)
        
        Detail_Frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE, bg="light gray")
        Detail_Frame.place(x=480, y=100, width=850, height=580)
        
        lbl_search = tk.Label(Detail_Frame, text="Search By:", bg="light gray", fg="black", font=("times new roman", 15, "bold"))
        lbl_search.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        
        search_combo = ttk.Combobox(Detail_Frame, textvariable=self.search_by_var, width=10, font=("times new roman", 13), state='readonly')
        search_combo['values'] = ('roll_number', 'name', 'phone')
        search_combo.grid(row=0, column=1, pady=10, padx=10)
        
        txt_search = tk.Entry(Detail_Frame, textvariable=self.search_txt_var, width=20, font=("times new roman", 13), bd=2, relief=tk.GROOVE)
        txt_search.grid(row=0, column=2, pady=10, padx=10, sticky="w")
        
        search_btn = tk.Button(Detail_Frame, text="Search", width=10, command=self.search_student)
        search_btn.grid(row=0, column=3, padx=5, pady=5)
        
        show_all_btn = tk.Button(Detail_Frame, text="Show All", width=10, command=self.display_data)
        show_all_btn.grid(row=0, column=4, padx=5, pady=5)

        table_frame = tk.Frame(Detail_Frame, bd=4, relief=tk.RIDGE, bg="white")
        table_frame.place(x=10, y=50, width=820, height=520)
        
        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        
        self.student_table = ttk.Treeview(
            table_frame, 
            columns=("roll_number", "name", "email", "phone", "gender", "dob", "address"), 
            xscrollcommand=scroll_x.set, 
            yscrollcommand=scroll_y.set
        )
        
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        headings = {
            "roll_number": "Roll No.", "name": "Name", "email": "Email", 
            "phone": "Contact No.", "gender": "Gender", "dob": "D.O.B", "address": "Address"
        }
        
        for col, text in headings.items():
            self.student_table.heading(col, text=text)
            self.student_table.column(col, width=100 if col != 'address' else 200, anchor=tk.CENTER)
            
        self.student_table['show'] = 'headings' 
        self.student_table.pack(fill=tk.BOTH, expand=True)
        
        self.student_table.bind("<ButtonRelease-1>", self.get_cursor)


    def add_student(self):
   
        if self.roll_var.get() == "" or self.name_var.get() == "":
            messagebox.showerror("Error", "Roll No. and Name are required!")
            return

        roll = self.roll_var.get()
        name = self.name_var.get()
        email = self.email_var.get()
        phone = self.phone_var.get()
        gender = self.gender_var.get()
        dob = self.dob_var.get()

        address = self.address_txt.get("1.0", tk.END).strip()

        if self.db.add_student(roll, name, email, phone, gender, dob, address):
            messagebox.showinfo("Success", "Student record added successfully!")
            self.clear_fields()
            self.display_data()

    def display_data(self):

        for item in self.student_table.get_children():
            self.student_table.delete(item)
            

        rows = self.db.fetch_students()
        for row in rows:
            self.student_table.insert('', tk.END, values=row)

    def get_cursor(self, event):

        cursor_row = self.student_table.focus()
        contents = self.student_table.item(cursor_row)
        row = contents['values']

        if row:
            self.clear_fields()
            self.roll_var.set(row[0])
            self.name_var.set(row[1])
            self.email_var.set(row[2])
            self.phone_var.set(row[3])
            self.gender_var.set(row[4])
            self.dob_var.set(row[5])
            
            self.address_txt.delete("1.0", tk.END)
            self.address_txt.insert("1.0", row[6])

    def update_student(self):
        roll = self.roll_var.get()
        if roll == "":
            messagebox.showerror("Error", "Select a record to update!")
            return
            
        name = self.name_var.get()
        email = self.email_var.get()
        phone = self.phone_var.get()
        gender = self.gender_var.get()
        dob = self.dob_var.get()
        address = self.address_txt.get("1.0", tk.END).strip()

        if self.db.update_student(roll, name, email, phone, gender, dob, address):
            messagebox.showinfo("Success", "Student record updated successfully!")
            self.clear_fields()
            self.display_data()

    def delete_student(self):
        roll = self.roll_var.get()
        if roll == "":
            messagebox.showerror("Error", "Select a record to delete!")
            return
            
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Roll No. {roll}?"):
            if self.db.delete_student(roll):
                messagebox.showinfo("Success", "Record deleted successfully!")
                self.clear_fields()
                self.display_data()

    def clear_fields(self):
        self.roll_var.set("")
        self.name_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.dob_var.set("")
        self.gender_var.set('Male') 
        self.address_txt.delete("1.0", tk.END)
        
    def search_student(self):
        key = self.search_by_var.get()
        value = self.search_txt_var.get()
        
        if not value:
            self.display_data()
            return
            
    
        rows = self.db.fetch_students(key, value)
        
        
        for item in self.student_table.get_children():
            self.student_table.delete(item)
            
        if not rows:
            messagebox.showinfo("Search Result", "No records found matching your criteria.")
        
        for row in rows:
            self.student_table.insert('', tk.END, values=row)


if __name__ == '__main__':
    root = tk.Tk()
    obj = StudentManagementSystem(root)
    root.mainloop()