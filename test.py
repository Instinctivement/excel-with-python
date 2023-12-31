import tkinter as tk
from tkinter import ttk
import os
import openpyxl

combo_list = ["Subscribed", "Not Subscribed", "Other"]

def toggle_mode():
    if mode_switch.instate(["selected"]):
        style.theme_use("forest-light")
    else:
        style.theme_use("forest-dark")

def load_data():
    data_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(data_dir, "people.xlsx")
    workbook = openpyxl.load_workbook(data_path)
    sheet = workbook.active
    
    list_values = list(sheet.values)
    for col_name in list_values[0]:
        treeview.heading(col_name, text=col_name)
    for value_tuple in list_values[1:]:
        treeview.insert('', tk.END, values=value_tuple)
def insert_row():
    name = name_entry.get()
    age = int(age_spinbox.get())
    subscription_status = status_combobox.get()
    employment_status = "Employed" if mycheck_var.get() else "Unemployed"
    
    # Insert row into Excel sheet
    data_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(data_dir, "people.xlsx")
    workbook = openpyxl.load_workbook(data_path)
    sheet = workbook.active
    row_values = [name, age, subscription_status, employment_status]
    
    sheet.append(row_values)
    workbook.save(data_path)
    
    # Insert row into treeview
    treeview.insert('', tk.END, values=row_values)
    
    # Clear the values
    name_entry.delete(0, "end")
    name_entry.insert(0, "Name")
    age_spinbox.delete(0, "end")
    age_spinbox.insert(0, "Age")
    status_combobox.set(combo_list[0])
    checkbutton.state(["!selected"])
    
    
    
root = tk.Tk()

# Définir le chemin d'accès relatif pour les fichiers de thème
theme_dir = os.path.dirname(os.path.abspath(__file__))
light_theme_path = os.path.join(theme_dir, "forest-light.tcl")
dark_theme_path = os.path.join(theme_dir, "forest-dark.tcl")

# Charger les fichiers de thème
root.tk.call("source", light_theme_path)
root.tk.call("source", dark_theme_path)

# Appliquer le thème foncé
style = ttk.Style(root)
style.theme_use("forest-dark")


frame = ttk.Frame(root)
frame.pack()

widgets_frame = ttk.LabelFrame(frame, text="Insert Row")
widgets_frame.grid(row=0, column=0, padx=20, pady=10)

name_entry = ttk.Entry(widgets_frame)
name_entry.insert(0, "Name")
name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
name_entry.grid(row=0, column=0, padx=5, pady=(10, 5), sticky="ew")

age_spinbox = ttk.Spinbox(widgets_frame, from_=18, to=100)
age_spinbox.insert(0, "Age")
age_spinbox.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

status_combobox = ttk.Combobox(widgets_frame, values=combo_list)
status_combobox.current(0)
status_combobox.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

mycheck_var = tk.BooleanVar()
checkbutton = ttk.Checkbutton(widgets_frame, text="Employed", variable=mycheck_var)
checkbutton.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

button = ttk.Button(widgets_frame, text="Insert", command=insert_row)
button.grid(row=4, column=0, padx=5, pady=(5, 10), sticky="nsew")

separator = ttk.Separator(widgets_frame)
separator.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

mode_switch = ttk.Checkbutton(widgets_frame, style="Switch", command=toggle_mode)
mode_switch.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

#/////////////////////////////////////////////////////

treeFrame = ttk.Frame(frame)
treeFrame.grid(row=0, column=1, pady=10)
treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")


cols=("Name", "Age", "Subscription", "Employment")
treeview = ttk.Treeview(treeFrame, show="headings", columns=cols, yscrollcommand=treeScroll.set, height=13)
treeview.column("Name", width=100)
treeview.column("Age", width=50)
treeview.column("Subscription", width=100)
treeview.column("Employment", width=100)
treeview.pack()
treeScroll.config(command=treeview.yview)

load_data()

root.mainloop()
