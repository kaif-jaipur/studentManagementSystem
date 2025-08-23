import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageFilter
from student import student
from storage import save_student, load_students, search_student, delete_student

import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def validate_age_input(text):
    """Validate that age input is numeric and within range."""
    if text == "" or (text.isdigit() and 0 < int(text) <= 120):
        return True
    return False

def validate_name_input(text):
    """Validate that name contains only letters and spaces."""
    if text == "" or all(c.isalpha() or c.isspace() for c in text):
        return True
    return False

def add_student():
    """Open a popup window to collect student details."""
    popup = tk.Toplevel(root)
    popup.title("Add New Student")
    popup.geometry("300x200")
    popup.transient(root)
    popup.grab_set()

    validate_age_popup = popup.register(validate_age_input)
    validate_name_popup = popup.register(validate_name_input)

    input_frame = ttk.LabelFrame(popup, text="Enter Student Details", padding=10)
    input_frame.pack(padx=10, pady=10, fill="both", expand=True)

    ttk.Label(input_frame, text="Name:", font=("Helvetica", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_name_popup = ttk.Entry(input_frame, width=20, font=("Helvetica", 10))
    entry_name_popup.grid(row=0, column=1, padx=5, pady=5)
    entry_name_popup.configure(validate="key", validatecommand=(validate_name_popup, "%P"))

    ttk.Label(input_frame, text="Age:", font=("Helvetica", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_age_popup = ttk.Entry(input_frame, width=20, font=("Helvetica", 10))
    entry_age_popup.grid(row=1, column=1, padx=5, pady=5)
    entry_age_popup.configure(validate="key", validatecommand=(validate_age_popup, "%P"))

    def submit_student():
        name = entry_name_popup.get().strip()
        age = entry_age_popup.get().strip()
        
        if not name or not age:
            messagebox.showwarning("Input Error", "Please enter both Name and Age", parent=popup)
            return
        
        try:
            age = int(age)
            if age <= 0 or age > 120:
                messagebox.showwarning("Input Error", "Please enter a valid age (1-120)", parent=popup)
                return
            if len(name) < 2:
                messagebox.showwarning("Input Error", "Name must be at least 2 characters", parent=popup)
                return
                
            s1 = student(name, age)
            save_student(s1)
            messagebox.showinfo("Success", f"Student {name} added successfully!", parent=popup)
            popup.destroy()
        except ValueError:
            messagebox.showwarning("Input Error", "Age must be a valid number", parent=popup)

    btn_submit = ttk.Button(input_frame, text="Submit", command=submit_student)
    btn_submit.grid(row=2, column=0, padx=5, pady=10)

    btn_cancel = ttk.Button(input_frame, text="Cancel", command=popup.destroy)
    btn_cancel.grid(row=2, column=1, padx=5, pady=10)

    entry_name_popup.focus_set()

def show_output_popup(students, title="Student List"):
    """Display student list in a popup window."""
    popup = tk.Toplevel(root)
    popup.title(title)
    popup.geometry("400x400")
    popup.transient(root)
    popup.grab_set()

    tree_frame = ttk.Frame(popup, padding=10)
    tree_frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Age"), show="headings", height=12)
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.column("ID", width=50, anchor="center")
    tree.column("Name", width=200, anchor="w")
    tree.column("Age", width=100, anchor="center")
    tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    for i, s in enumerate(students, 1):
        tree.insert("", tk.END, values=(i, s.name, s.age))

    btn_close = ttk.Button(popup, text="Close", command=popup.destroy)
    btn_close.pack(pady=10)

def search_student_gui():
    """Open a popup with blurred background to collect search query with Search, Clear Search, and Cancel buttons."""
    popup = tk.Toplevel(root)
    popup.title("Search Student")
    popup.geometry("300x250")
    popup.transient(root)
    popup.grab_set()

    # Create canvas for blurred background image
    canvas_popup = tk.Canvas(popup, width=300, height=250)
    canvas_popup.pack(fill="both", expand=True)

    # Load, blur, and set background image
    try:
        bg_image = Image.open(resource_path("back_ground.jpeg"))
        bg_image = bg_image.resize((300, 250), Image.Resampling.LANCZOS)
        bg_image = bg_image.filter(ImageFilter.GaussianBlur(radius=5))
        bg_photo_popup = ImageTk.PhotoImage(bg_image)
        canvas_popup.create_image(0, 0, image=bg_photo_popup, anchor="nw")
        popup.bg_photo_popup = bg_photo_popup
    except Exception as e:
        print(f"Error loading background image in popup: {e}")
        canvas_popup.configure(bg="#f0f0f0")

    # Create a solid frame for readability
    search_frame = tk.Frame(popup, bg="#2E2E2E")
    canvas_popup.create_window(150, 125, window=search_frame, anchor="center")

    ttk.Label(search_frame, text="Enter student name to search:", font=("Helvetica", 10), background="#2E2E2E", foreground="white").pack(pady=5)
    entry_search_popup = ttk.Entry(search_frame, width=20, font=("Helvetica", 10))
    entry_search_popup.pack(pady=5)
    entry_search_popup.focus_set()

    def perform_search():
        query = entry_search_popup.get().strip()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a search query", parent=popup)
            return
        
        results = search_student(query)
        if results:
            popup.destroy()
            show_output_popup(results, "Search Results")
        else:
            messagebox.showinfo("Info", "No students found!", parent=popup)

    def clear_search():
        entry_search_popup.delete(0, tk.END)

    # Button frame to align buttons horizontally
    button_frame = ttk.Frame(search_frame)
    button_frame.pack(pady=10)

    btn_search = ttk.Button(button_frame, text="Search", command=perform_search)
    btn_search.pack(side="left", padx=5)

    btn_clear = ttk.Button(button_frame, text="Clear Search", command=clear_search)
    btn_clear.pack(side="left", padx=5)

    btn_cancel = ttk.Button(button_frame, text="Cancel", command=popup.destroy)
    btn_cancel.pack(side="left", padx=5)

def delete_student_gui():
    """Open a popup with blurred background to collect student name for deletion."""
    popup = tk.Toplevel(root)
    popup.title("Delete Student")
    popup.geometry("300x250")
    popup.transient(root)
    popup.grab_set()

    # Create canvas for blurred background image
    canvas_popup = tk.Canvas(popup, width=300, height=250)
    canvas_popup.pack(fill="both", expand=True)

    # Load, blur, and set background image
    try:
        bg_image = Image.open(resource_path("back_ground.jpeg"))
        bg_image = bg_image.resize((300, 250), Image.Resampling.LANCZOS)
        bg_image = bg_image.filter(ImageFilter.GaussianBlur(radius=5))
        bg_photo_popup = ImageTk.PhotoImage(bg_image)
        canvas_popup.create_image(0, 0, image=bg_photo_popup, anchor="nw")
        popup.bg_photo_popup = bg_photo_popup
    except Exception as e:
        print(f"Error loading background image in popup: {e}")
        canvas_popup.configure(bg="#f0f0f0")

    # Create a solid frame for readability
    delete_frame = tk.Frame(popup, bg="#2E2E2E")
    canvas_popup.create_window(150, 125, window=delete_frame, anchor="center")

    ttk.Label(delete_frame, text="Enter student name to delete:", font=("Helvetica", 10), background="#2E2E2E", foreground="white").pack(pady=5)
    entry_delete_popup = ttk.Entry(delete_frame, width=20, font=("Helvetica", 10))
    entry_delete_popup.pack(pady=5)
    entry_delete_popup.focus_set()

    def perform_delete():
        query = entry_delete_popup.get().strip()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a student name", parent=popup)
            return

        results = search_student(query)  # returns list of student objects

        if not results:
            messagebox.showinfo("Info", "No students found!", parent=popup)
            return

        if len(results) > 1:
            # Popup for selection
            select_popup = tk.Toplevel(popup)
            select_popup.title("Select Student to Delete")
            select_popup.geometry("400x350")
            select_popup.transient(popup)
            select_popup.grab_set()

            tk.Label(select_popup, text="Multiple students found! Please select one to delete:").pack(pady=(10, 2))

            tree = ttk.Treeview(select_popup, columns=("Index", "Name", "Age"), show="headings")
            tree.heading("Index", text="Index")
            tree.heading("Name", text="Name")
            tree.heading("Age", text="Age")
            tree.column("Index", width=50, anchor="center")
            tree.column("Name", width=200, anchor="w")
            tree.column("Age", width=100, anchor="center")
            tree.pack(padx=10, pady=(2, 10), fill="both", expand=True)

            # Fill treeview with matching students
            for i, s in enumerate(results, 1):
                tree.insert("", tk.END, values=(i, s.name, s.age))

            button_frame = ttk.Frame(select_popup)
            button_frame.pack(fill="x", side="bottom", pady=10)
            
            def confirm_single_delete():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Selection Error", "Please select a student to delete", parent=select_popup)
                    return
                item = tree.item(selected[0])
                idx = int(item["values"][0]) - 1
                student_to_delete = results[idx]  # This is the exact student object

                try:
                    delete_student(student_to_delete)  # Pass the student object
                    messagebox.showinfo("Success", f"Student {student_to_delete.name} deleted successfully!", parent=select_popup)
                    select_popup.destroy()
                    popup.destroy()  # Close both popups after successful deletion
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete student: {e}", parent=select_popup)

            btn_confirm = ttk.Button(button_frame, text="Delete Selected Student", command=confirm_single_delete)
            btn_confirm.pack(side="left", padx=20)
            btn_cancel = ttk.Button(button_frame, text="Cancel", command=select_popup.destroy)
            btn_cancel.pack(side="right", padx=20)
            tree.focus_set()
            return

        # Only one student found, delete directly
        try:
            delete_student(results[0])  # Pass the student object
            messagebox.showinfo("Success", f"Student {results[0].name} deleted successfully!", parent=popup)
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete student: {e}", parent=popup)

    def clear_delete():
        entry_delete_popup.delete(0, tk.END)

    # Button frame to align buttons horizontally
    button_frame = ttk.Frame(delete_frame)
    button_frame.pack(pady=10)

    btn_delete = ttk.Button(button_frame, text="Delete", command=perform_delete)
    btn_delete.pack(side="left", padx=5)

    btn_clear = ttk.Button(button_frame, text="Clear", command=clear_delete)
    btn_clear.pack(side="left", padx=5)

    btn_cancel = ttk.Button(button_frame, text="Cancel", command=popup.destroy)
    btn_cancel.pack(side="left", padx=5)

def show_all():
    """Display all students in a popup window."""
    students = load_students()
    if not students:
        messagebox.showinfo("Info", "No students found!")
        return
    show_output_popup(students, "All Students")

def exit_app():
    """Confirm before exiting the application."""
    if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
        root.destroy()

# Hover effect functions
def on_enter(button, hover_color):
    button.config(bg=hover_color, highlightthickness=3)

def on_leave(button, original_color):
    button.config(bg=original_color, highlightthickness=2)

# GUI Window
root = tk.Tk()
root.title("Student Management System")
root.geometry("700x600")

# Create a canvas for the background image
canvas = tk.Canvas(root, width=700, height=600)
canvas.grid(row=0, column=0, rowspan=3, columnspan=1, sticky="nsew")

# Load and set background image
try:
    bg_image = Image.open(resource_path("back_ground.jpeg"))
    bg_image = bg_image.resize((700, 600), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
except Exception as e:
    print(f"Error loading background image: {e}")
    canvas.configure(bg="#f0f0f0")  # Fallback background color

# Style configuration for ttk widgets
style = ttk.Style()
style.configure("Treeview", font=("Helvetica", 10))
style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
style.configure("TEntry", font=("Helvetica", 11))
style.configure("TButton", font=("Helvetica", 11, "bold"))

# Background panel for controls
panel = tk.Frame(root, bg="#2E2E2E")
canvas.create_window(350, 250, window=panel, anchor="center", width=300, height=300)

# Title directly on canvas
title_label = tk.Label(root, text="Student Management System", font=("Helvetica", 24, "bold"), fg="red", bg="black")
canvas.create_window(350, 50, window=title_label, anchor="n")

# Buttons with professional styling
button_width = 22
button_style = {
    "font": ("Helvetica", 12, "bold"),
    "fg": "white",
    "relief": "flat",
    "padx": 20,
    "pady": 10,
    "highlightthickness": 2,
    "highlightbackground": "#2E2E2E",
    "width": button_width
}

# Button positions (centered column, vertical stacking)
y_start = 120
y_spacing = 60

btn_add = tk.Button(panel, text="Add Student", bg="#26A69A", activebackground="#239d90", **button_style, command=add_student)
btn_add.grid(row=0, column=0, padx=10, pady=10)
btn_add.bind("<Enter>", lambda e: on_enter(btn_add, "#239d90"))
btn_add.bind("<Leave>", lambda e: on_leave(btn_add, "#26A69A"))

btn_search = tk.Button(panel, text="Search Student", bg="#757575", activebackground="#676767", **button_style, command=search_student_gui)
btn_search.grid(row=1, column=0, padx=10, pady=10)
btn_search.bind("<Enter>", lambda e: on_enter(btn_search, "#676767"))
btn_search.bind("<Leave>", lambda e: on_leave(btn_search, "#757575"))

btn_show = tk.Button(panel, text="Show All Students", bg="#757575", activebackground="#676767", **button_style, command=show_all)
btn_show.grid(row=2, column=0, padx=10, pady=10)
btn_show.bind("<Enter>", lambda e: on_enter(btn_show, "#676767"))
btn_show.bind("<Leave>", lambda e: on_leave(btn_show, "#757575"))

btn_delete = tk.Button(panel, text="Delete Student", bg="#EF5350", activebackground="#e53935", **button_style, command=delete_student_gui)
btn_delete.grid(row=3, column=0, padx=10, pady=10)
btn_delete.bind("<Enter>", lambda e: on_enter(btn_delete, "#e53935"))
btn_delete.bind("<Leave>", lambda e: on_leave(btn_delete, "#EF5350"))

btn_exit = tk.Button(panel, text="Exit", bg="#EF5350", activebackground="#e53935", **button_style, command=exit_app)
btn_exit.grid(row=4, column=0, padx=10, pady=10)
btn_exit.bind("<Enter>", lambda e: on_enter(btn_exit, "#e53935"))
btn_exit.bind("<Leave>", lambda e: on_leave(btn_exit, "#EF5350"))

canvas.create_window(350, 250, window=panel, anchor="center")

# Keep reference to photo to prevent garbage collection
root.bg_photo = bg_photo

root.mainloop()