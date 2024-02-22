'''
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import ttk
import mysql.connector
from datetime import datetime

class PlantManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Plant Management System")
        self.geometry("800x600")
        self.configure(bg="#2b2b2b")

        self.db = mysql.connector.connect(host='localhost', user='root', password='3372', database='plant')
        self.mycursor = self.db.cursor()

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Plant Management System", font=("Arial", 20), bg="#2b2b2b", fg="white")
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.text_area = scrolledtext.ScrolledText(self, width=70, height=10, bg="#1e1e1e", fg="white")
        self.text_area.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.add_frame = tk.Frame(self, bg="#2b2b2b")
        self.add_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        ttk.Label(self.add_frame, text="Plant ID:", background="#2b2b2b", foreground="white").grid(row=0, column=0, sticky="e", pady=5)
        ttk.Label(self.add_frame, text="Plant Name:", background="#2b2b2b", foreground="white").grid(row=1, column=0, sticky="e", pady=5)
        ttk.Label(self.add_frame, text="Plant Type:", background="#2b2b2b", foreground="white").grid(row=2, column=0, sticky="e", pady=5)
        ttk.Label(self.add_frame, text="Watering Schedule:", background="#2b2b2b", foreground="white").grid(row=3, column=0, sticky="e", pady=5)
        ttk.Label(self.add_frame, text="Special Considerations:", background="#2b2b2b", foreground="white").grid(row=4, column=0, sticky="e", pady=5)
        ttk.Label(self.add_frame, text="Planted On (yyyy-mm-dd):", background="#2b2b2b", foreground="white").grid(row=5, column=0, sticky="e", pady=5)

        self.plant_id_entry = ttk.Entry(self.add_frame)
        self.plant_id_entry.grid(row=0, column=1, pady=5)
        self.plant_name_entry = ttk.Entry(self.add_frame)
        self.plant_name_entry.grid(row=1, column=1, pady=5)
        self.plant_type_entry = ttk.Entry(self.add_frame)
        self.plant_type_entry.grid(row=2, column=1, pady=5)
        self.watering_schedule_entry = ttk.Entry(self.add_frame)
        self.watering_schedule_entry.grid(row=3, column=1, pady=5)
        self.special_consideration_entry = ttk.Entry(self.add_frame)
        self.special_consideration_entry.grid(row=4, column=1, pady=5)
        self.planted_on_entry = ttk.Entry(self.add_frame)
        self.planted_on_entry.grid(row=5, column=1, pady=5)

        self.button_add = ttk.Button(self.add_frame, text="Add Plant Details", command=self.add_dtl)
        self.button_add.grid(row=6, columnspan=2, pady=10)

        self.button_display = ttk.Button(self, text="Display Plant Details", command=self.display_details)
        self.button_display.grid(row=3, column=0, padx=10, pady=10)

        self.button_specific = ttk.Button(self, text="Display Specific Details", command=self.display_specific_details)
        self.button_specific.grid(row=3, column=1, padx=10, pady=10)

        self.button_water = ttk.Button(self, text="Water Plants", command=self.water)
        self.button_water.grid(row=4, column=0, padx=10, pady=10)

        self.button_delete = ttk.Button(self, text="Delete Plant Record", command=self.delete_record)
        self.button_delete.grid(row=4, column=1, padx=10, pady=10)

        self.button_edit = ttk.Button(self, text="Edit Plant Details", command=self.edit_details)
        self.button_edit.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.button_exit = ttk.Button(self, text="Exit", command=self.destroy)
        self.button_exit.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def add_dtl(self):
        plant_id = self.plant_id_entry.get()
        plant_name = self.plant_name_entry.get()
        plant_type = self.plant_type_entry.get()
        watering_schedule = self.watering_schedule_entry.get()
        special_consideration = self.special_consideration_entry.get()
        planted_on = self.planted_on_entry.get()

        try:
            self.mycursor.execute("INSERT INTO plant_detail (plant_id, plant_name, plant_type, watering_schedule, special_consideration, planted_on) VALUES (%s, %s, %s, %s, %s, %s)",
                                  (plant_id, plant_name, plant_type, watering_schedule, special_consideration, planted_on))
            self.db.commit()
            messagebox.showinfo("Success", "Plant details added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {e}")

    def display_details(self):
        self.text_area.delete('1.0', tk.END)
        try:
            self.mycursor.execute("SELECT * FROM plant_detail A, plant_progress B WHERE A.plant_id = B.plant_id")
            details = self.mycursor.fetchall()
            for detail in details:
                self.text_area.insert(tk.END, f"{detail}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {e}")

    def display_specific_details(self):
        self.text_area.delete('1.0', tk.END)
        plant_id = self.plant_id_entry.get()
        try:
            self.mycursor.execute("SELECT * FROM plant_detail A, plant_progress B WHERE A.plant_id = B.plant_id AND A.plant_id = %s", (plant_id,))
            detail = self.mycursor.fetchone()
            self.text_area.insert(tk.END, f"Plant details: {detail}\n")
            current_watering_status = datetime.strptime(str(detail[8]), "%Y-%m-%d")
            current_date = datetime.now()
            difference = current_date - current_watering_status
            result = difference.days
            self.text_area.insert(tk.END, f"Days without water: {result}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {e}")

    def water(self):
        self.text_area.delete('1.0', tk.END)
        self.display_details()
        plant_id = self.plant_id_entry.get()

        formatted_date = datetime.now().strftime("%Y-%m-%d")
        try:
            self.mycursor.execute("UPDATE plant_progress SET current_watering_status = %s WHERE plant_id = %s", (formatted_date, plant_id))
            self.db.commit()
            messagebox.showinfo("Success", "Plant has been watered!")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {e}")

    def delete_record(self):
        self.text_area.delete('1.0', tk.END)
        plant_id = self.plant_id_entry.get()
        try:
            self.mycursor.execute("DELETE FROM plant_progress WHERE plant_id = %s", (plant_id,))
            self.db.commit()
            self.mycursor.execute("DELETE FROM plant_detail WHERE plant_id = %s", (plant_id,))
            self.db.commit()
            messagebox.showinfo("Success", f"Record with plant ID {plant_id} deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {e}")

    def edit_details(self):
        self.text_area.delete('1.0', tk.END)
        self.display_details()
        plant_id = self.plant_id_entry.get()
        choice = input("Select Choice:\n1. Plant Name\n2. Plant Type\n3. Watering Schedule\n4. Special Consideration\n")

        if choice == '1':
            name = input("Enter new plant name: ")
            try:
                self.mycursor.execute("UPDATE plant_detail SET plant_name = %s WHERE plant_id = %s", (name, plant_id))
                self.db.commit()
                messagebox.showinfo("Success", "Plant name updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error occurred: {e}")

        # Similarly handle other choices

if __name__ == "__main__":
    app = PlantManagerApp()
    app.mainloop()
'''
'''
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import ttk
import mysql.connector
from datetime import datetime

class AddPlantWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Add Plant Details")
        self.geometry("400x300")
        self.configure(bg="#2b2b2b")

        self.label = tk.Label(self, text="Add Plant Details", font=("Arial", 16), bg="#2b2b2b", fg="white")
        self.label.pack(pady=10)

        self.frame = tk.Frame(self, bg="#2b2b2b")
        self.frame.pack(padx=10, pady=10)

        ttk.Label(self.frame, text="Plant ID:", background="#2b2b2b", foreground="white").grid(row=0, column=0, sticky="e", pady=5)
        ttk.Label(self.frame, text="Plant Name:", background="#2b2b2b", foreground="white").grid(row=1, column=0, sticky="e", pady=5)
        ttk.Label(self.frame, text="Plant Type:", background="#2b2b2b", foreground="white").grid(row=2, column=0, sticky="e", pady=5)
        ttk.Label(self.frame, text="Watering Schedule:", background="#2b2b2b", foreground="white").grid(row=3, column=0, sticky="e", pady=5)
        ttk.Label(self.frame, text="Special Considerations:", background="#2b2b2b", foreground="white").grid(row=4, column=0, sticky="e", pady=5)
        ttk.Label(self.frame, text="Planted On (yyyy-mm-dd):", background="#2b2b2b", foreground="white").grid(row=5, column=0, sticky="e", pady=5)

        self.plant_id_entry = ttk.Entry(self.frame)
        self.plant_id_entry.grid(row=0, column=1, pady=5)
        self.plant_name_entry = ttk.Entry(self.frame)
        self.plant_name_entry.grid(row=1, column=1, pady=5)
        self.plant_type_entry = ttk.Entry(self.frame)
        self.plant_type_entry.grid(row=2, column=1, pady=5)
        self.watering_schedule_entry = ttk.Entry(self.frame)
        self.watering_schedule_entry.grid(row=3, column=1, pady=5)
        self.special_consideration_entry = ttk.Entry(self.frame)
        self.special_consideration_entry.grid(row=4, column=1, pady=5)
        self.planted_on_entry = ttk.Entry(self.frame)
        self.planted_on_entry.grid(row=5, column=1, pady=5)

        self.button_add = ttk.Button(self, text="Add Plant Details", command=self.add_dtl)
        self.button_add.pack(pady=10)

    def add_dtl(self):
        plant_id = self.plant_id_entry.get()
        plant_name = self.plant_name_entry.get()
        plant_type = self.plant_type_entry.get()
        watering_schedule = self.watering_schedule_entry.get()
        special_consideration = self.special_consideration_entry.get()
        planted_on = self.planted_on_entry.get()

        try:
            self.parent.mycursor.execute("INSERT INTO plant_detail (plant_id, plant_name, plant_type, watering_schedule, special_consideration, planted_on) VALUES (%s, %s, %s, %s, %s, %s)",
                                  (plant_id, plant_name, plant_type, watering_schedule, special_consideration, planted_on))
            self.parent.db.commit()
            messagebox.showinfo("Success", "Plant details added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {e}")


class DisplayPlantDetailsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Display Plant Details")
        self.geometry("600x400")
        self.configure(bg="#2b2b2b")

        self.label = tk.Label(self, text="Plant Details", font=("Arial", 16), bg="#2b2b2b", fg="white")
        self.label.pack(pady=10)

        self.text_area = scrolledtext.ScrolledText(self, width=70, height=10, bg="#1e1e1e", fg="white")
        self.text_area.pack(padx=10, pady=10)

        self.display_details()

    def display_details(self):
        self.text_area.delete('1.0', tk.END)
        try:
            self.parent.mycursor.execute("SELECT * FROM plant_detail A, plant_progress B WHERE A.plant_id = B.plant_id")
            details = self.parent.mycursor.fetchall()
            for detail in details:
                self.text_area.insert(tk.END, f"{detail}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {e}")


class PlantManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Plant Management System")
        self.geometry("800x600")
        self.configure(bg="#2b2b2b")

        self.db = mysql.connector.connect(host='localhost', user='root', password='3372', database='plant')
        self.mycursor = self.db.cursor()

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Plant Management System", font=("Arial", 20), bg="#2b2b2b", fg="white")
        self.label.pack(pady=10)

        self.button_add = ttk.Button(self, text="Add Plant Details", command=self.open_add_window)
        self.button_add.pack(pady=10)

        self.button_display = ttk.Button(self, text="Display Plant Details", command=self.open_display_window)
        self.button_display.pack(pady=10)

    def open_add_window(self):
        add_window = AddPlantWindow(self)
        add_window.grab_set()  # Make the window modal

    def open_display_window(self):
        display_window = DisplayPlantDetailsWindow(self)
        display_window.grab_set()  # Make the window modal


if __name__ == "__main__":
    app = PlantManagerApp()
    app.mainloop()
'''
