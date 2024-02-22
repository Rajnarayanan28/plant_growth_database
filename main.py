import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import mysql.connector
from datetime import datetime, timedelta

# Establish database connection
db = mysql.connector.connect(host='localhost', user='root', password='3372', database='plant')
mycursor = db.cursor()

def create():
    try:
        mycursor.execute("create table plant_detail (plant_id varchar(10) Primary key ,plant_name varchar(20),plant_type varchar(20),watering_schedule int,Special_consideration varchar(30),planted_on date)")
        mycursor.execute("create table plant_progress (plant_id varchar(10) Primary key,plant_name varchar(20),current_watering_status date)")
    except:
        print("File exists")
        
create()
# Tkinter App
class PlantManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Plant Management System")
        self.geometry("800x600")
        self.configure(bg="#2b2b2b")

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Plant Management System", font=("Arial", 20), bg="#2b2b2b", fg="white")
        self.label.pack(pady=10)

        self.button_add = tk.Button(self, text="Add Plant Details", command=self.add_dtl_window)
        self.button_add.pack(pady=10)

        self.button_display = tk.Button(self, text="Display Plant Details", command=self.display_details)
        self.button_display.pack(pady=10)

        self.button_water = tk.Button(self, text="Water Plants", command=self.water_window)
        self.button_water.pack(pady=10)

        self.button_delete = tk.Button(self, text="Delete Plant Record", command=self.delete_window)
        self.button_delete.pack(pady=10)

        self.button_edit = tk.Button(self, text="Edit Plant Details", command=self.edit_details_window)
        self.button_edit.pack(pady=10)

        self.button_display_specific = tk.Button(self, text="Display Specific", command=self.display_specific_window)
        self.button_display_specific.pack(pady=10)

    def add_dtl_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add Plant Details")
        add_window.geometry("400x300")

        label = tk.Label(add_window, text="Add Plant Details", font=("Arial", 16))
        label.pack(pady=10)

        frame = tk.Frame(add_window)
        frame.pack(padx=10, pady=10)

        ttk.Label(frame, text="Plant ID:").grid(row=0, column=0, sticky="e", pady=5)
        ttk.Label(frame, text="Plant Name:").grid(row=1, column=0, sticky="e", pady=5)
        ttk.Label(frame, text="Plant Type:").grid(row=2, column=0, sticky="e", pady=5)
        ttk.Label(frame, text="Watering Schedule:").grid(row=3, column=0, sticky="e", pady=5)
        ttk.Label(frame, text="Special Considerations:").grid(row=4, column=0, sticky="e", pady=5)
        ttk.Label(frame, text="Planted On (yyyy-mm-dd):").grid(row=5, column=0, sticky="e", pady=5)

        plant_id_entry = ttk.Entry(frame)
        plant_id_entry.grid(row=0, column=1, pady=5)
        plant_name_entry = ttk.Entry(frame)
        plant_name_entry.grid(row=1, column=1, pady=5)
        plant_type_entry = ttk.Entry(frame)
        plant_type_entry.grid(row=2, column=1, pady=5)
        watering_schedule_entry = ttk.Entry(frame)
        watering_schedule_entry.grid(row=3, column=1, pady=5)
        special_consideration_entry = ttk.Entry(frame)
        special_consideration_entry.grid(row=4, column=1, pady=5)
        planted_on_entry = ttk.Entry(frame)
        planted_on_entry.grid(row=5, column=1, pady=5)

        button_add = ttk.Button(add_window, text="Add Plant Details", command=lambda: self.add_dtl(
            plant_id_entry.get(), plant_name_entry.get(), plant_type_entry.get(),
            watering_schedule_entry.get(), special_consideration_entry.get(), planted_on_entry.get()
        ))
        button_add.pack(pady=10)

    def add_dtl(self, plant_id, plant_name, plant_type, watering_schedule, special_consideration, planted_on):
        current_watering_status = planted_on

        try:
            mycursor.execute("INSERT INTO plant_detail (plant_id, plant_name, plant_type, watering_schedule, special_consideration, planted_on) VALUES (%s, %s, %s, %s, %s, %s)",
                              (plant_id, plant_name, plant_type, watering_schedule, special_consideration, planted_on))
            mycursor.execute("INSERT INTO plant_progress (plant_id, plant_name, current_watering_status) VALUES (%s, %s, %s)",
                             (plant_id, plant_name, current_watering_status))
            db.commit()
            messagebox.showinfo("Success", "Plant details added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {e}")

    def display_details(self):  # Add 'self' as the first parameter
        mycursor.execute("SELECT * FROM plant_detail A, plant_progress B WHERE A.plant_id = B.plant_id")
        
        display_window = tk.Toplevel()
        display_window.title("Display Plant Details")
        display_window.geometry("800x400")

        label = tk.Label(display_window, text="Plant Details", font=("Arial", 16))
        label.pack(pady=10)

        tree = ttk.Treeview(display_window, columns=("Plant ID", "Plant Name", "Plant Type", "Watering Schedule", "Special Considerations", "Planted On", "Need Water"), show="headings", selectmode="browse")

        # Define column headings
        tree.heading("Plant ID", text="Plant ID")
        tree.heading("Plant Name", text="Plant Name")
        tree.heading("Plant Type", text="Plant Type")
        tree.heading("Watering Schedule", text="Watering Schedule")
        tree.heading("Special Considerations", text="Special Considerations")
        tree.heading("Planted On", text="Planted On")
        tree.heading("Need Water", text="Need Water")

        # Define column widths
        tree.column("Plant ID", width=100)
        tree.column("Plant Name", width=100)
        tree.column("Plant Type", width=100)
        tree.column("Watering Schedule", width=150)
        tree.column("Special Considerations", width=150)
        tree.column("Planted On", width=100)
        tree.column("Need Water", width=100)

        tree.pack(fill="both", expand=True)

        try:
            for rec in mycursor:
                # Calculate if the plant needs water
                start_date = rec[-1]
                days_to_add = rec[3]
                delta = timedelta(days=days_to_add)
                result_date = start_date + delta  
                current_date = datetime.now()
                difference = current_date - result_date
                need_water = "Yes" if difference.days > 0 else "No"
                
                # Insert the plant details into the treeview
                tree.insert("", "end", values=(*rec, need_water))
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {e}")

    def display_details(self):
        mycursor.execute("SELECT * FROM plant_detail A, plant_progress B WHERE A.plant_id = B.plant_id")
        
        display_window = tk.Toplevel()
        display_window.title("Display Plant Details")
        display_window.geometry("800x400")

        label = tk.Label(display_window, text="Plant Details", font=("Arial", 16))
        label.pack(pady=10)

        tree = ttk.Treeview(display_window, columns=("Plant ID", "Plant Name", "Plant Type", "Watering Schedule", "Special Considerations", "Planted On", "Need Water"), show="headings", selectmode="browse")

        # Define column headings
        tree.heading("Plant ID", text="Plant ID")
        tree.heading("Plant Name", text="Plant Name")
        tree.heading("Plant Type", text="Plant Type")
        tree.heading("Watering Schedule", text="Watering Schedule")
        tree.heading("Special Considerations", text="Special Considerations")
        tree.heading("Planted On", text="Planted On")
        tree.heading("Need Water", text="Need Water")

        # Define column widths
        tree.column("Plant ID", width=100)
        tree.column("Plant Name", width=100)
        tree.column("Plant Type", width=100)
        tree.column("Watering Schedule", width=150)
        tree.column("Special Considerations", width=150)
        tree.column("Planted On", width=100)
        tree.column("Need Water", width=100)

        tree.pack(fill="both", expand=True)

        try:
            for rec in mycursor:
                # Convert start_date to datetime.datetime
                start_date = datetime.combine(rec[-1], datetime.min.time())
                days_to_add = rec[3]
                delta = timedelta(days=days_to_add)
                result_date = start_date + delta
                current_date = datetime.now()
                
                # Calculate if the plant needs water
                difference = current_date - result_date
                need_water = "Yes" if difference.days > 0 else "No"
                
                # Insert the plant details into the treeview
                tree.insert("", "end", values=(*rec[:6], need_water))
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {e}")
                
    def water_window(self):
        water_window = tk.Toplevel(self)
        water_window.title("Water Plants")
        water_window.geometry("400x200")

        label = tk.Label(water_window, text="Water Plants", font=("Arial", 16))
        label.pack(pady=10)

        plant_id_label = ttk.Label(water_window, text="Plant ID:")
        plant_id_label.pack(pady=5)
        plant_id_entry = ttk.Entry(water_window)
        plant_id_entry.pack(pady=5)

        button_water = ttk.Button(water_window, text="Water Plant", command=lambda: self.water(plant_id_entry.get()))
        button_water.pack(pady=10)

    def water(self, plant_id):
        formatted_date = datetime.now().strftime("%Y-%m-%d")
        try:
            mycursor.execute("UPDATE plant_progress SET current_watering_status = %s WHERE plant_id = %s", (formatted_date, plant_id))
            db.commit()
            messagebox.showinfo("Success", "Plant has been watered!")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {e}")

    def delete_window(self):
        delete_window = tk.Toplevel(self)
        delete_window.title("Delete Plant Record")
        delete_window.geometry("300x150")

        label = tk.Label(delete_window, text="Delete Plant Record", font=("Arial", 16))
        label.pack(pady=10)

        plant_id_label = ttk.Label(delete_window, text="Plant ID:")
        plant_id_label.pack(pady=5)
        plant_id_entry = ttk.Entry(delete_window)
        plant_id_entry.pack(pady=5)

        button_delete = ttk.Button(delete_window, text="Delete Record", command=lambda: self.delete_record(plant_id_entry.get()))
        button_delete.pack(pady=5)

    def delete_record(self, plant_id):
        try:
            mycursor.execute("DELETE FROM plant_progress WHERE plant_id = %s", (plant_id,))
            db.commit()
            mycursor.execute("DELETE FROM plant_detail WHERE plant_id = %s", (plant_id,))
            db.commit()
            messagebox.showinfo("Success", f"Record with plant ID {plant_id} deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred while deleting record: {e}")

    def edit_details_window(self):
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Plant Details")
        edit_window.geometry("400x200")

        label = tk.Label(edit_window, text="Edit Plant Details", font=("Arial", 16))
        label.pack(pady=10)

        plant_id_label = ttk.Label(edit_window, text="Plant ID:")
        plant_id_label.pack(pady=5)
        plant_id_entry = ttk.Entry(edit_window)
        plant_id_entry.pack(pady=5)

        button_edit = ttk.Button(edit_window, text="Edit Details", command=lambda: self.edit_details(plant_id_entry.get()))
        button_edit.pack(pady=10)

    def edit_details(self, plant_id):
        try:
            mycursor.execute("SELECT * FROM plant_detail WHERE plant_id = %s", (plant_id,))
            plant_details = mycursor.fetchone()
            if plant_details:
                edit_window = tk.Toplevel(self)
                edit_window.title("Edit Plant Details")
                edit_window.geometry("400x300")

                label = tk.Label(edit_window, text="Edit Plant Details", font=("Arial", 16))
                label.pack(pady=10)

                frame = tk.Frame(edit_window)
                frame.pack(padx=10, pady=10)

                # Populate entry fields with existing values
                plant_name_entry = ttk.Entry(frame)
                plant_name_entry.insert(0, plant_details[1])
                plant_name_entry.grid(row=0, column=1, pady=5)

                plant_type_entry = ttk.Entry(frame)
                plant_type_entry.insert(0, plant_details[2])
                plant_type_entry.grid(row=1, column=1, pady=5)

                watering_schedule_entry = ttk.Entry(frame)
                watering_schedule_entry.insert(0, plant_details[3])
                watering_schedule_entry.grid(row=2, column=1, pady=5)

                special_consideration_entry = ttk.Entry(frame)
                special_consideration_entry.insert(0, plant_details[4])
                special_consideration_entry.grid(row=3, column=1, pady=5)

                button_update = ttk.Button(edit_window, text="Update Details", command=lambda: self.update_details(plant_id, plant_name_entry.get(), plant_type_entry.get(), watering_schedule_entry.get(), special_consideration_entry.get()))
                button_update.pack(pady=10)
            else:
                messagebox.showinfo("Plant Details", "No data found for the specified plant ID.")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {e}")


    def update_details(self, plant_id, plant_name, plant_type, watering_schedule, special_consideration):
        try:
            mycursor.execute("UPDATE plant_detail SET plant_name = %s, plant_type = %s, watering_schedule = %s, special_consideration = %s WHERE plant_id = %s", (plant_name, plant_type, watering_schedule, special_consideration, plant_id))
            db.commit()
            messagebox.showinfo("Success", "Plant details updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred while updating details: {e}")

    def display_specific_window(self):
        display_specific_window = tk.Toplevel(self)
        display_specific_window.title("Display Specific Plant Details")
        display_specific_window.geometry("500x200")

        label = tk.Label(display_specific_window, text="Display Specific Plant Details", font=("Arial", 16))
        label.pack(pady=10)

        plant_id_label = ttk.Label(display_specific_window, text="Plant ID:")
        plant_id_label.pack(pady=5)
        plant_id_entry = ttk.Entry(display_specific_window)
        plant_id_entry.pack(pady=5)

        button_display_specific = ttk.Button(display_specific_window, text="Display", command=lambda: self.display_specific_details(plant_id_entry.get()))
        button_display_specific.pack(pady=10)

    def display_specific_details(self, plant_id):
        try:
            mycursor.execute("SELECT * FROM plant_detail A, plant_progress B WHERE A.plant_id = B.plant_id AND A.plant_id = %s", (plant_id,))
            plant_details = mycursor.fetchone()
            if plant_details:
                messagebox.showinfo("Plant Details",
                                    f"Plant ID: {plant_details[0]}\nPlant Name: {plant_details[1]}\nPlant Type: {plant_details[2]}\nWatering Schedule: {plant_details[3]}\nSpecial Considerations: {plant_details[4]}\nPlanted On: {plant_details[5]}\nCurrent Watering Status: {plant_details[8]}")
            else:
                messagebox.showinfo("Plant Details", "No data found for the specified plant ID.")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {e}")

if __name__ == "__main__":
    app = PlantManagerApp()
    app.mainloop()
