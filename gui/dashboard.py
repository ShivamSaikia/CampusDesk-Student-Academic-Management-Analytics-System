import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser
from database.db import DatabaseManager
from utils.validator import validate_student_id, validate_email, validate_phone, validate_marks, calculate_grade
from utils.file_manager import export_csv, export_json, ensure_dir
from utils.report_generator import generate_html_report

class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CampusDesk Dashboard")
        self.geometry("1100x700")
        self.db = DatabaseManager()
        self.configure(padx=10, pady=10)
        self.build_ui()
        self.refresh_students()

    def build_ui(self):
        title = tk.Label(self, text="CampusDesk", font=("Arial", 24, "bold"))
        title.pack(anchor="w")
        tk.Label(self, text="Student Academic Management System").pack(anchor="w")

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, pady=15)

        self.student_tab = ttk.Frame(self.tabs)
        self.marks_tab = ttk.Frame(self.tabs)
        self.att_tab = ttk.Frame(self.tabs)
        self.report_tab = ttk.Frame(self.tabs)

        self.tabs.add(self.student_tab, text="Students")
        self.tabs.add(self.marks_tab, text="Marks")
        self.tabs.add(self.att_tab, text="Attendance")
        self.tabs.add(self.report_tab, text="Reports & Analytics")

        self.build_students()
        self.build_marks()
        self.build_attendance()
        self.build_reports()

    def build_students(self):
        form = ttk.LabelFrame(self.student_tab, text="Student Details")
        form.pack(fill="x", padx=10, pady=10)

        labels = ["Student ID", "Name", "Email", "Course", "Semester", "Phone"]
        self.student_entries = {}
        for i, label in enumerate(labels):
            ttk.Label(form, text=label).grid(row=i//3*2, column=i%3, padx=8, pady=(8,2), sticky="w")
            e = ttk.Entry(form, width=25)
            e.grid(row=i//3*2+1, column=i%3, padx=8, pady=(0,8))
            self.student_entries[label] = e

        buttons = ttk.Frame(self.student_tab)
        buttons.pack(fill="x", padx=10)
        ttk.Button(buttons, text="Add", command=self.add_student).pack(side="left", padx=4)
        ttk.Button(buttons, text="Update", command=self.update_student).pack(side="left", padx=4)
        ttk.Button(buttons, text="Delete", command=self.delete_student).pack(side="left", padx=4)
        ttk.Button(buttons, text="Clear", command=self.clear_student).pack(side="left", padx=4)

        search_frame = ttk.Frame(self.student_tab)
        search_frame.pack(fill="x", padx=10, pady=10)
        ttk.Label(search_frame, text="Search").pack(side="left")
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side="left", padx=8)
        ttk.Button(search_frame, text="Search", command=self.refresh_students).pack(side="left")

        cols = ("ID","Name","Email","Course","Semester","Phone")
        self.student_tree = ttk.Treeview(self.student_tab, columns=cols, show="headings")
        for c in cols:
            self.student_tree.heading(c, text=c)
            self.student_tree.column(c, width=140)
        self.student_tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.student_tree.bind("<<TreeviewSelect>>", self.select_student)

    def add_student(self):
        try:
            vals = [self.student_entries[x].get().strip() for x in self.student_entries]
            sid, name, email, course, semester, phone = vals
            if not validate_student_id(sid):
                raise ValueError("Student ID must look like STU001.")
            if not name or not course:
                raise ValueError("Name and course are required.")
            if not validate_email(email):
                raise ValueError("Enter a valid email.")
            if not validate_phone(phone):
                raise ValueError("Phone must contain 10 digits.")
            semester = int(semester)
            if not 1 <= semester <= 12:
                raise ValueError("Semester must be between 1 and 12.")
            self.db.add_student((sid.upper(), name, email, course, semester, phone))
            messagebox.showinfo("Success", "Student added.")
            self.clear_student()
            self.refresh_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_student(self):
        try:
            vals = [self.student_entries[x].get().strip() for x in self.student_entries]
            sid, name, email, course, semester, phone = vals
            if not validate_student_id(sid) or not validate_email(email) or not validate_phone(phone):
                raise ValueError("Please enter valid student details.")
            self.db.update_student((sid, name, email, course, int(semester), phone))
            messagebox.showinfo("Success", "Student updated.")
            self.refresh_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_student(self):
        sid = self.student_entries["Student ID"].get().strip()
        if not sid:
            messagebox.showwarning("Select", "Select a student first.")
            return
        if messagebox.askyesno("Confirm", f"Delete {sid}?"):
            self.db.delete_student(sid)
            self.clear_student()
            self.refresh_students()

    def clear_student(self):
        for e in self.student_entries.values():
            e.delete(0, tk.END)

    def select_student(self, _event=None):
        selected = self.student_tree.selection()
        if not selected:
            return
        values = self.student_tree.item(selected[0], "values")
        for key, value in zip(self.student_entries, values):
            self.student_entries[key].delete(0, tk.END)
            self.student_entries[key].insert(0, value)

    def refresh_students(self):
        if not hasattr(self, "student_tree"):
            return
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        for row in self.db.get_students(self.search_var.get() if hasattr(self, "search_var") else ""):
            self.student_tree.insert("", "end", values=row)

    def build_marks(self):
        form = ttk.LabelFrame(self.marks_tab, text="Marks Entry")
        form.pack(fill="x", padx=10, pady=10)
        labels = ["Student ID","Subject","Internal","Assignment","Lab","End Semester"]
        self.mark_entries = {}
        for i, label in enumerate(labels):
            ttk.Label(form, text=label).grid(row=0, column=i, padx=6, pady=4)
            e = ttk.Entry(form, width=16)
            e.grid(row=1, column=i, padx=6, pady=4)
            self.mark_entries[label] = e
        ttk.Button(form, text="Save Marks", command=self.add_marks).grid(row=1, column=6, padx=8)

        cols=("ID","Subject","Internal","Assignment","Lab","End Sem","Total","Grade")
        self.mark_tree=ttk.Treeview(self.marks_tab,columns=cols,show="headings")
        for c in cols:
            self.mark_tree.heading(c,text=c)
            self.mark_tree.column(c,width=115)
        self.mark_tree.pack(fill="both",expand=True,padx=10,pady=10)

    def add_marks(self):
        try:
            e=self.mark_entries
            sid=e["Student ID"].get().strip().upper()
            vals=[e[x].get().strip() for x in ["Internal","Assignment","Lab","End Semester"]]
            if not validate_marks(*vals):
                raise ValueError("Marks must be numbers between 0 and 100.")
            if not sid or not e["Subject"].get().strip():
                raise ValueError("Student ID and subject are required.")
            nums=list(map(float,vals))
            total=sum(nums)/4
            grade=calculate_grade(total)
            self.db.add_marks((sid,e["Subject"].get().strip(),*nums,total,grade))
            self.refresh_marks()
            messagebox.showinfo("Saved",f"Total: {total:.2f} | Grade: {grade}")
        except Exception as ex:
            messagebox.showerror("Error",str(ex))

    def refresh_marks(self):
        for item in self.mark_tree.get_children():
            self.mark_tree.delete(item)
        for row in self.db.get_marks():
            self.mark_tree.insert("", "end", values=row)

    def build_attendance(self):
        form=ttk.LabelFrame(self.att_tab,text="Attendance Entry")
        form.pack(fill="x",padx=10,pady=10)
        labels=["Student ID","Subject","Total Classes","Attended"]
        self.att_entries={}
        for i,label in enumerate(labels):
            ttk.Label(form,text=label).grid(row=0,column=i,padx=10,pady=4)
            e=ttk.Entry(form,width=20)
            e.grid(row=1,column=i,padx=10,pady=4)
            self.att_entries[label]=e
        ttk.Button(form,text="Save Attendance",command=self.add_attendance).grid(row=1,column=4,padx=10)

        cols=("ID","Subject","Total","Attended","Percentage")
        self.att_tree=ttk.Treeview(self.att_tab,columns=cols,show="headings")
        for c in cols:
            self.att_tree.heading(c,text=c)
            self.att_tree.column(c,width=150)
        self.att_tree.pack(fill="both",expand=True,padx=10,pady=10)

    def add_attendance(self):
        try:
            e=self.att_entries
            sid=e["Student ID"].get().strip().upper()
            total=int(e["Total Classes"].get())
            attended=int(e["Attended"].get())
            if total<=0 or attended<0 or attended>total:
                raise ValueError("Attendance values are invalid.")
            percentage=attended/total*100
            self.db.add_attendance((sid,e["Subject"].get().strip(),total,attended,percentage))
            self.refresh_attendance()
            messagebox.showinfo("Saved",f"Attendance: {percentage:.2f}%")
        except Exception as ex:
            messagebox.showerror("Error",str(ex))

    def refresh_attendance(self):
        for item in self.att_tree.get_children():
            self.att_tree.delete(item)
        for row in self.db.get_attendance():
            self.att_tree.insert("", "end", values=row)

    def build_reports(self):
        frame=ttk.Frame(self.report_tab)
        frame.pack(fill="both",expand=True,padx=20,pady=20)
        self.analytics=tk.StringVar(value="Loading...")
        ttk.Label(frame,text="Academic Analytics",font=("Arial",20,"bold")).pack(pady=10)
        ttk.Label(frame,textvariable=self.analytics,font=("Arial",14)).pack(pady=20)
        ttk.Button(frame,text="Refresh Analytics",command=self.update_analytics).pack(pady=5)
        ttk.Button(frame,text="Export Students CSV",command=self.export_students).pack(pady=5)
        ttk.Button(frame,text="Export Students JSON",command=self.export_students_json).pack(pady=5)
        ttk.Button(frame,text="Generate HTML Report",command=self.generate_report_async).pack(pady=5)
        self.update_analytics()

    def update_analytics(self):
        students,passed,avg_marks,avg_att=self.db.counts()
        self.analytics.set(
            f"Total Students: {students}\n"
            f"Passed Mark Records: {passed}\n"
            f"Average Marks: {avg_marks:.2f}\n"
            f"Average Attendance: {avg_att:.2f}%"
        )

    def export_students(self):
        ensure_dir("reports")
        rows=self.db.get_students()
        export_csv("reports/students.csv",["ID","Name","Email","Course","Semester","Phone"],rows)
        messagebox.showinfo("Exported","reports/students.csv created.")

    def export_students_json(self):
        ensure_dir("reports")
        rows=self.db.get_students()
        export_json("reports/students.json",["ID","Name","Email","Course","Semester","Phone"],rows)
        messagebox.showinfo("Exported","reports/students.json created.")

    def generate_report_async(self):
        # Demonstrates multithreading so the GUI remains responsive.
        def task():
            filename=generate_html_report(
                self.db.get_students(), self.db.get_marks(), self.db.get_attendance()
            )
            self.after(0,lambda:self.report_done(filename))
        threading.Thread(target=task,daemon=True).start()

    def report_done(self,filename):
        messagebox.showinfo("Report Ready",f"Created: {filename}")
        webbrowser.open(filename)
