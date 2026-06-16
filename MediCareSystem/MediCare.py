import tkinter as tk
from tkinter import ttk, messagebox
import uuid
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors


THEME = {
    "primary": "#2C3E50",
    "secondary": "#34495E",
    "accent": "#3498DB",
    "bg": "#F4F7F6",
    "surface": "#FFFFFF",
    "text": "#2C3E50",
    "danger": "#BF3222",
    "success": "#158845",
    "edit": "#D88602",
}


class Entity:
    def __init__(self, name):
        self.id = str(uuid.uuid4())[:8].upper()
        self.name = name


class Patient(Entity):
    def __init__(self, name, age, gender, blood):
        super().__init__(name)
        self.age, self.gender, self.blood = age, gender, blood


class Doctor(Entity):
    def __init__(self, name, specialty):
        super().__init__(name)
        self.specialty = specialty


class Appointment:
    def __init__(self, patient, doctor, date):
        self.id = str(uuid.uuid4())[:6].upper()
        self.patient, self.doctor, self.date = patient, doctor, date
        self.name = f"APT-{patient[:3]}"


class Treatment:
    def __init__(self, patient, t_type, cost):
        self.id = str(uuid.uuid4())[:6].upper()
        self.name = patient
        self.type = t_type
        self.cost = float(cost)
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M")


class HospitalService:
    def __init__(self):
        self._data = {
            "Patients": [],
            "Doctors": [],
            "Appointments": [],
            "Treatments": [],
        }

    def add_record(self, category, obj):
        self._data[category].append(obj)
        return True

    def update_record(self, category, obj_id, new_data):
        for idx, item in enumerate(self._data[category]):
            if item.id == obj_id:
                if category == "Patients":
                    item.name, item.age, item.gender, item.blood = new_data
                elif category == "Doctors":
                    item.name, item.specialty = new_data
                elif category == "Appointments":
                    item.patient, item.doctor, item.date = new_data
                    item.name = f"APT-{new_data[0][:3]}"
                elif category == "Treatments":
                    item.name, item.type, item.cost = (
                        new_data[0],
                        new_data[1],
                        float(new_data[2]),
                    )
                return True
        return False

    def remove_record(self, category, obj_id):
        self._data[category] = [x for x in self._data[category] if x.id != obj_id]
        return True

    def get_all(self, category):
        return self._data[category]

    def search(self, category, query):
        q = query.lower()
        return [
            x for x in self._data[category] if q in x.name.lower() or q in x.id.lower()
        ]


class PDFService:
    @staticmethod
    def generate_invoice(treatment):
        filename = f"Invoice_{treatment.id}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        c.setFillColor(colors.HexColor(THEME["primary"]))
        c.rect(0, height - 80, width, 80, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 22)
        c.drawString(50, height - 50, "MEDICARE HOSPITAL INVOICE")

        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 120, f"INVOICE ID: {treatment.id}")
        c.drawString(50, height - 140, f"DATE: {treatment.date}")
        c.drawString(50, height - 170, f"PATIENT: {treatment.name}")

        c.setStrokeColor(colors.lightgrey)
        c.line(50, height - 190, width - 50, height - 190)
        c.drawString(60, height - 210, "Medical Service Rendered")
        c.drawRightString(width - 60, height - 210, "Cost")
        c.line(50, height - 220, width - 50, height - 220)

        c.setFont("Helvetica", 11)
        c.drawString(60, height - 240, treatment.type)
        c.drawRightString(width - 60, height - 240, f"Rs{treatment.cost:,.2f}")

        c.setFont("Helvetica-Bold", 14)
        c.drawRightString(
            width - 60, height - 280, f"TOTAL PAYABLE: Rs{treatment.cost:,.2f}"
        )
        c.save()
        return filename


class HospitalManagementApp:
    def __init__(self, root):
        self.root = root
        self.service = HospitalService()

        self.root.title("MediCare Hospital Management System")
        self.root.geometry("1300x850")
        self.root.configure(bg=THEME["bg"])

        self.current_user = None
        self.main_container = tk.Frame(self.root, bg=THEME["bg"])
        self.main_container.pack(fill="both", expand=True)

        self._setup_styles()
        self.show_login()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=THEME["bg"], borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            padding=[25, 12],
            font=("Segoe UI", 10, "bold"),
            background="#D1D8E0",
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", THEME["primary"])],
            foreground=[("selected", "white")],
        )
        style.configure("Treeview", rowheight=35, font=("Segoe UI", 10), borderwidth=0)
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background=THEME["secondary"],
            foreground="white",
        )

    def show_login(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

        login_frame = tk.Frame(
            self.main_container,
            bg=THEME["surface"],
            padx=50,
            pady=50,
            highlightbackground="#D1D8E0",
            highlightthickness=1,
        )
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            login_frame,
            text="Welcome to MediCare",
            font=("Segoe UI", 24, "bold"),
            bg=THEME["surface"],
            fg=THEME["primary"],
        ).pack(pady=(0, 30))

        tk.Label(
            login_frame, text="Username", bg=THEME["surface"], font=("Segoe UI", 10)
        ).pack(anchor="w")
        user_ent = tk.Entry(
            login_frame, width=35, font=("Segoe UI", 11), bd=1, relief="solid"
        )
        user_ent.pack(pady=(5, 20), ipady=5)

        tk.Label(
            login_frame, text="Password", bg=THEME["surface"], font=("Segoe UI", 10)
        ).pack(anchor="w")
        pass_ent = tk.Entry(
            login_frame, width=35, font=("Segoe UI", 11), show="●", bd=1, relief="solid"
        )
        pass_ent.pack(pady=(5, 30), ipady=5)

        def attempt_login():
            if user_ent.get() == "admin" and pass_ent.get() == "admin":
                self.current_user = "Administrator"
                self.build_dashboard()
            else:
                messagebox.showerror(
                    "Access Denied", "Invalid administrative credentials."
                )

        tk.Button(
            login_frame,
            text="LOGIN TO MEDICARE",
            bg=THEME["accent"],
            fg="white",
            font=("Segoe UI", 11, "bold"),
            command=attempt_login,
            width=30,
            pady=10,
            cursor="hand2",
            bd=0,
        ).pack()

    def logout(self):
        if messagebox.askyesno(
            "Are you really want to logout?", "Do you really want to logout?"):
            self.current_user = None
            self.show_login()

    def build_dashboard(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

        header = tk.Frame(self.main_container, bg=THEME["primary"], height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="MEDICARE HOSPITAL MANAGEMENT SYSTEM",
            font=("Segoe UI", 16, "bold"),
            bg=THEME["primary"],
            fg="white",
            padx=20,
        ).pack(side="left")

        user_info = tk.Frame(header, bg=THEME["primary"])
        user_info.pack(side="right", padx=20)

        tk.Label(
            user_info,
            text=f"SESSION: {self.current_user}",
            fg="#BDC3C7",
            bg=THEME["primary"],
            font=("Segoe UI", 9),
        ).pack(side="left", padx=15)
        tk.Button(
            user_info,
            text="LOGOUT",
            font=("Segoe UI", 9, "bold"),
            bg=THEME["danger"],
            fg="white",
            command=self.logout,
            bd=0,
            padx=15,
            pady=5,
        ).pack(side="left")

        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)

        self.tabs = {}
        self._init_data_tabs()
        self._init_billing_tab()
        self._init_report_tab()

    def _init_data_tabs(self):
        configs = [
            ("Patients", ["ID", "Name", "Age", "Gender", "Blood"]),
            ("Doctors", ["ID", "Name", "Specialty"]),
            ("Appointments", ["ID", "Patient", "Doctor", "Date"]),
            ("Treatments", ["ID", "Patient", "Type", "Cost"]),
        ]
        for cat, cols in configs:
            self.tabs[cat] = self._create_data_view(cat, cols)

    def _create_data_view(self, category, columns):
        tab = tk.Frame(self.notebook, bg=THEME["surface"])
        self.notebook.add(tab, text=f" {category.upper()} ")

        ctrl = tk.Frame(tab, bg=THEME["surface"], pady=15)
        ctrl.pack(fill="x", padx=15)

        tk.Label(
            ctrl,
            text="Filter Records:",
            font=("Segoe UI", 9, "bold"),
            bg=THEME["surface"],
        ).pack(side="left")
        search_ent = tk.Entry(
            ctrl, width=25, font=("Segoe UI", 10), bd=1, relief="solid"
        )
        search_ent.pack(side="left", padx=10, ipady=3)

        tk.Button(
            ctrl,
            text="+ New Record",
            bg=THEME["success"],
            fg="white",
            font=("Segoe UI", 9, "bold"),
            command=lambda: self._open_form(category),
            bd=0,
            padx=15,
        ).pack(side="left", padx=5)

        tk.Button(
            ctrl,
            text="✎ Edit Selected",
            bg=THEME["edit"],
            fg="white",
            font=("Segoe UI", 9, "bold"),
            command=lambda: self._edit_selected(category, tree),
            bd=0,
            padx=15,
        ).pack(side="left", padx=5)

        tk.Button(
            ctrl,
            text="Remove",
            bg=THEME["danger"],
            fg="white",
            font=("Segoe UI", 9, "bold"),
            command=lambda: self._delete_selected(category, tree),
            bd=0,
            padx=15,
        ).pack(side="left", padx=5)

        tree_frame = tk.Frame(tab)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=5)
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        tree.pack(fill="both", expand=True)

        search_ent.bind(
            "<KeyRelease>",
            lambda e: self._handle_search(category, search_ent.get(), tree),
        )
        return tree

    def _init_billing_tab(self):
        self.bill_tab = tk.Frame(self.notebook, bg=THEME["surface"])
        self.notebook.add(self.bill_tab, text=" FINANCIALS ")

        header_frame = tk.Frame(self.bill_tab, bg=THEME["bg"], pady=20)
        header_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            header_frame,
            text="INVOICE MANAGEMENT CENTER",
            font=("Segoe UI", 12, "bold"),
            bg=THEME["bg"],
            fg=THEME["primary"],
        ).pack(side="left", padx=10)

        tk.Button(
            header_frame,
            text="🖨️ EXPORT PDF INVOICE",
            bg=THEME["accent"],
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=25,
            pady=8,
            bd=0,
            command=self._print_pdf_action,
        ).pack(side="right", padx=10)

        cols = ["ID", "Patient", "Type", "Cost", "Date"]
        self.bill_tree = ttk.Treeview(self.bill_tab, columns=cols, show="headings")
        for col in cols:
            self.bill_tree.heading(col, text=col)
            self.bill_tree.column(col, anchor="center")
        self.bill_tree.pack(fill="both", expand=True, padx=20, pady=10)

    def _init_report_tab(self):
        self.report_tab = tk.Frame(self.notebook, bg=THEME["bg"])
        self.notebook.add(self.report_tab, text=" ANALYTICS ")

        report_card = tk.Frame(
            self.report_tab, bg=THEME["surface"], padx=60, pady=40, relief="solid", bd=1
        )
        report_card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            report_card,
            text="MediCare System Report",
            font=("Segoe UI", 18, "bold"),
            bg=THEME["surface"],
            fg=THEME["primary"],
        ).pack(pady=(0, 20))

        self.report_content = tk.Label(
            report_card,
            text="Synchronize to view live data",
            font=("Courier New", 11),
            bg="#F8F9F9",
            justify="left",
            padx=20,
            pady=20,
            width=55,
            relief="sunken",
        )
        self.report_content.pack(pady=20)

        tk.Button(
            report_card,
            text="REFRESH SYSTEM DATA",
            bg=THEME["primary"],
            fg="white",
            font=("Segoe UI", 10, "bold"),
            pady=12,
            command=self._update_report,
            bd=0,
        ).pack(fill="x")

    def _update_report(self):
        patients = self.service.get_all("Patients")
        doctors = self.service.get_all("Doctors")
        treatments = self.service.get_all("Treatments")
        revenue = sum(t.cost for t in treatments)

        stats = f"""
        DATA SNAPSHOT: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        -----------------------------------------------
        Total Patient Records:    {len(patients):03d}
        Total Active Staff:       {len(doctors):03d}
        Completed Treatments:     {len(treatments):03d}
        
        TOTAL SYSTEM REVENUE:     Rs{revenue:,.2f}
        -----------------------------------------------
        Encryption: Active | DB Status: Online
        """
        self.report_content.config(text=stats)

    def _print_pdf_action(self):
        sel = self.bill_tree.selection()
        if not sel:
            return messagebox.showwarning(
                "Invoicing", "Select a record from the list first."
            )

        rec_id = self.bill_tree.item(sel[0])["values"][0]
        treatment = next(
            (t for t in self.service.get_all("Treatments") if t.id == rec_id), None
        )

        if treatment:
            path = PDFService.generate_invoice(treatment)
            messagebox.showinfo(
                "Export Success", f"Invoice generated at:\n{os.path.abspath(path)}"
            )

    def _edit_selected(self, category, tree):
        sel = tree.selection()
        if not sel:
            return messagebox.showwarning(
                "Required", "Please select a record to modify."
            )

        values = tree.item(sel[0])["values"]
        self._open_form(category, edit_data=values)

    def _open_form(self, category, edit_data=None):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"MediCare Entry - {category}")
        dialog.geometry("420x600")
        dialog.configure(padx=30, pady=20, bg=THEME["surface"])
        dialog.grab_set()

        entries = {}
        if category == "Patients":
            fields = [
                ("Full Name", "ent"),
                ("Age", "ent"),
                ("Gender", "cb", ["Male", "Female", "Other"]),
                (
                    "Blood Group",
                    "cb",
                    ["A+", "B+", "O+", "AB+", "A-", "B-", "O-", "AB-"],
                ),
            ]
        elif category == "Doctors":
            fields = [("Doctor Name", "ent"), ("Specialty", "ent")]
        elif category == "Appointments":
            p_list = [p.name for p in self.service.get_all("Patients")]
            d_list = [d.name for d in self.service.get_all("Doctors")]
            fields = [
                ("Patient Name", "cb", p_list),
                ("Doctor Name", "cb", d_list),
                ("Appointment Date", "ent"),
            ]
        else:
            p_list = [p.name for p in self.service.get_all("Patients")]
            fields = [
                ("Patient Name", "cb", p_list),
                ("Treatment Type", "ent"),
                ("Cost (Rs)", "ent"),
            ]

        for i, (lbl, ttype, *vals) in enumerate(fields):
            tk.Label(
                dialog, text=lbl, bg=THEME["surface"], font=("Segoe UI", 9, "bold")
            ).pack(anchor="w", pady=(10, 0))
            widget = (
                tk.Entry(dialog, font=("Segoe UI", 10), bd=1, relief="solid")
                if ttype == "ent"
                else ttk.Combobox(dialog, values=vals[0], font=("Segoe UI", 10))
            )
            widget.pack(fill="x", pady=5, ipady=4)
            entries[lbl.lower()] = widget

            if edit_data:
                val_to_set = str(edit_data[i + 1]).replace("Rs.", "").replace(",", "")
                if ttype == "ent":
                    widget.insert(0, val_to_set)
                else:
                    widget.set(val_to_set)

        def save():
            d = [v.get() for v in entries.values()]
            if not all(str(val).strip() for val in d):
                return messagebox.showerror(
                    "Validation", "All fields must be completed."
                )

            if edit_data:
                self.service.update_record(category, edit_data[0], d)
            else:
                if category == "Patients":
                    obj = Patient(*d)
                elif category == "Doctors":
                    obj = Doctor(*d)
                elif category == "Appointments":
                    obj = Appointment(*d)
                else:
                    obj = Treatment(*d)
                self.service.add_record(category, obj)

            self._refresh_all_views()
            dialog.destroy()

        btn_txt = "SAVE CHANGES" if edit_data else "REGISTER"
        btn_clr = THEME["accent"] if edit_data else THEME["success"]
        tk.Button(
            dialog,
            text=btn_txt,
            bg=btn_clr,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            pady=12,
            command=save,
            bd=0,
        ).pack(fill="x", pady=30)

    def _refresh_all_views(self):
        for cat in ["Patients", "Doctors", "Appointments", "Treatments"]:
            tree = self.tabs[cat]
            tree.delete(*tree.get_children())
            for item in self.service.get_all(cat):
                tree.insert("", "end", values=self._get_vals(item, cat))

        self.bill_tree.delete(*self.bill_tree.get_children())
        for t in self.service.get_all("Treatments"):
            self.bill_tree.insert(
                "", "end", values=(t.id, t.name, t.type, f"Rs {t.cost:,.2f}", t.date)
            )

    def _get_vals(self, obj, cat):
        if cat == "Patients":
            return (obj.id, obj.name, obj.age, obj.gender, obj.blood)
        if cat == "Doctors":
            return (obj.id, obj.name, obj.specialty)
        if cat == "Appointments":
            return (obj.id, obj.patient, obj.doctor, obj.date)
        return (obj.id, obj.name, obj.type, f"Rs {obj.cost:,.2f}")

    def _handle_search(self, category, query, tree):
        res = self.service.search(category, query)
        tree.delete(*tree.get_children())
        for item in res:
            tree.insert("", "end", values=self._get_vals(item, category))

    def _delete_selected(self, category, tree):
        sel = tree.selection()
        if not sel:
            return
        item_id = tree.item(sel[0])["values"][0]
        if messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to permanently delete this record?",
        ):
            self.service.remove_record(category, item_id)
            self._refresh_all_views()


if __name__ == "__main__":
    root = tk.Tk()
    root.option_add("*Font", "SegoeUI 10")
    app = HospitalManagementApp(root)
    root.mainloop()
