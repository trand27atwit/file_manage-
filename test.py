from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import os
from datetime import datetime

# Initialize SQLite database
def initialize_db():
    conn = sqlite3.connect('file_organization.db')
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        keywords TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subcategories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        path TEXT NOT NULL,
        type TEXT,
        size INTEGER,
        last_modified TIMESTAMP,
        category_id INTEGER,
        subcategory_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories (id),
        FOREIGN KEY (subcategory_id) REFERENCES subcategories (id)
    )
    ''')

    conn.commit()
    conn.close()

# Function to refresh the category section in the UI
def refreshCategorySection():
    category_tree.delete(*category_tree.get_children())  # Clear existing entries
    conn = sqlite3.connect('file_organization.db')
    cursor = conn.cursor()

    # Get categories
    cursor.execute('SELECT id, name FROM categories')
    categories = cursor.fetchall()
    category_map = {}

    # Insert categories into treeview and store item reference
    for cat_id, cat_name in categories:
        category_map[cat_id] = category_tree.insert("", "end", text=cat_name, values=("Category"))

    # Get subcategories and place them under the right category
    cursor.execute('SELECT name, category_id FROM subcategories')
    subcategories = cursor.fetchall()
    for sub_name, category_id in subcategories:
        if category_id in category_map:
            category_tree.insert(category_map[category_id], "end", text=sub_name, values=("Subcategory"))

    conn.close()

def delete():
    selected_item = category_tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a category or subcategory to delete.")
        return
    
    category_name = category_tree.item(selected_item, 'text')
    
    if not category_name:
        return
    
    response = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{category_name}'?")
    if response:
        conn = sqlite3.connect('file_organization.db')
        cursor = conn.cursor()
        
        # Delete category and related subcategories/files
        cursor.execute('DELETE FROM files WHERE category_id IN (SELECT id FROM categories WHERE name = ?)', (category_name,))
        cursor.execute('DELETE FROM subcategories WHERE category_id IN (SELECT id FROM categories WHERE name = ?)', (category_name,))
        cursor.execute('DELETE FROM categories WHERE name = ?', (category_name,))
        
        conn.commit()
        conn.close()
        
        refreshCategorySection()

# Function to open the "New Category" window
def categoryWin():
    c_window = Toplevel(root)
    c_window.title('New Category')
    c_window.geometry('400x300')

    c_window.columnconfigure(0, weight=1)

    # Name label
    cname_label = Label(c_window, text="Name:")
    cname_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Name entry field
    cname_entry = Entry(c_window, width=30)
    cname_entry.grid(row=0, column=1, padx=10, pady=10)

    # Keywords label
    ckeyword_label = Label(c_window, text="Keywords")
    ckeyword_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    # Keywords entry field
    ckeyword_entry = Entry(c_window, width=30)
    ckeyword_entry.grid(row=1, column=1, padx=10, pady=10)

    # Function to handle category creation
    def categoryCreation():
        name = cname_entry.get().strip()
        keywords = ckeyword_entry.get().strip()

        if not name: 
            messagebox.showwarning("Warning," "Please enter a category name. ")
            return

        conn = sqlite3.connect('file_organization.db')
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO categories (name, keywords) VALUES (?, ?)', (name, keywords))
            conn.commit()
            c_window.destroy()
            refreshCategorySection()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", f"A category with this name already exists.")
        finally:
            conn.close()

    # Create button
    create_button = Button(c_window, text="Create", command=categoryCreation)
    create_button.grid(row=4, column=1, columnspan=2, pady=10)

# Function to open the "New SubCategory" window
def subcategoryWin():
    sub_window = Toplevel(root)
    sub_window.title('New SubCategory')
    sub_window.geometry('400x300')

    # Category Label
    subc_label = Label(sub_window, text="Category:")
    subc_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Dropdown for Category Selection
    conn = sqlite3.connect('file_organization.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM categories')
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()

    subc_dropdown = ttk.Combobox(sub_window, values=categories, state="readonly", width=27)
    subc_dropdown.grid(row=0, column=1, padx=10, pady=10)
    subc_dropdown.current(0)  # Set default selection

    # Name label
    subname_label = Label(sub_window, text="Subcategory Name:")
    subname_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    # Name entry field
    subname_entry = Entry(sub_window, width=30)
    subname_entry.grid(row=1, column=1, padx=10, pady=10)

    # Function to handle subcategory creation
    def subcategoryCreation():
        category_name = subc_dropdown.get()
        subcategory_name = subname_entry.get().strip()

        conn = sqlite3.connect('file_organization.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM categories WHERE name = ?', (category_name,))
        category_id = cursor.fetchone()[0]
        cursor.execute('INSERT INTO subcategories (name, category_id) VALUES (?, ?)', (subcategory_name, category_id))
        conn.commit()
        conn.close()

        sub_window.destroy()
        refreshCategorySection()

    # Create button
    create_button = Button(sub_window, text="Create", command=subcategoryCreation)
    create_button.grid(row=4, column=1, columnspan=2, pady=10)

def redirectWin():
    red_window = Toplevel(root)
    red_window.title('Redirect')
    red_window.geometry('400x300')

    red_window.columnconfigure(0, weight=1)

    # File Location
    redl_label = Label(red_window, text="File Location:")
    redl_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

     # Dropdown for File Location Selection
    redname_entry = Entry(red_window, width=30)
    redname_entry.grid(row=0, column=1, padx=10, pady=10)

    # Category Label
    redc_label = Label(red_window, text="Category:")
    redc_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    # Dropdown for Category Selection
    subname_entry = Entry(red_window, width=30)
    subname_entry.grid(row=1, column=1, padx=10, pady=10)

    # Subcategory label
    subname_label = Label(red_window, text="Subcategory Name:")
    subname_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    # Dropdown for Category Selection
    subname_entry = Entry(red_window, width=30)
    subname_entry.grid(row=2, column=1, padx=10, pady=10)


def renameWin():
    ren_window = Toplevel(root)
    ren_window.title('Rename')
    ren_window.geometry('400x300')

    ren_window.columnconfigure(0, weight=1)

    # Category Label
    renc_label = Label(ren_window, text="Category:")
    renc_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    # Dropdown for Category Selection
    subname_entry = Entry(ren_window, width=30)
    subname_entry.grid(row=1, column=1, padx=10, pady=10)

    # Subcategory label
    rens_label = Label(ren_window, text="Subcategory Name:")
    rens_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    # Dropdown for Category Selection
    rens_entry = Entry(ren_window, width=30)
    rens_entry.grid(row=2, column=1, padx=10, pady=10)

def modifyFilterWin():
    modF_window = Toplevel(root)
    modF_window.title('New SubCategory')
    modF_window.geometry('400x300')

    # Category Label
    modFi_label = Label(modF_window, text="Category:")
    modFi_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Dropdown for Category Selection
    categories = ["Food", "Electronics", "Clothing", "Books"]  # Example categories
    modFi_dropdown = ttk.Combobox(modF_window, values=categories, state="readonly", width=27)
    modFi_dropdown.grid(row=0, column=1, padx=10, pady=10)
    modFi_dropdown.current(0)  # Set default selection

    # Name label
    modFname_label = Label(modF_window, text="Subcategory Name:")
    modFname_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    # Name entry field
    modFname_entry = Entry(modF_window, width=30)
    modFname_entry.grid(row=1, column=1, padx=10, pady=10)


# Root window
root = Tk()
root.title('Easy Find')
root.geometry('600x400')

# Initialize the database
initialize_db()

# Create the menu bar
menubar = Menu(root)
root.config(menu=menubar)

# Create the "New" menu
new_menu = Menu(menubar, tearoff=0)
new_menu.add_command(label='New Category', command=categoryWin)
new_menu.add_command(label='New Subcategory', command=subcategoryWin)
menubar.add_cascade(label='New', menu=new_menu)

# Create the "Modify" menu
modify_menu = Menu(menubar, tearoff=0)
modify_menu.add_command(label='Redirect', command=redirectWin)
modify_menu.add_command(label='Rename', command=renameWin)
modify_menu.add_command(label='Modify Filter', command=modifyFilterWin)
menubar.add_cascade(label='Modify', menu=modify_menu)

# Create the "Delete" menu
delete_menu = Menu(menubar, tearoff=0)
delete_menu.add_command(label='Delete', command=delete)
menubar.add_cascade(label='Delete', menu=delete_menu)

# Create the "Search" menu
search_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Search', menu=search_menu)

# Main frame section
main_frame = Frame(root)
main_frame.pack(fill="both", expand=True)

# File section
file_frame = Frame(main_frame)
file_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

# File Treeview
file_tree = ttk.Treeview(file_frame, columns=("Type", "Date"), show="tree headings")
file_tree.heading("#0", text="Name")
file_tree.heading("Type", text="Type")
file_tree.heading("Date", text="Date")
file_tree.pack(fill="both", expand=True)

# Category section
category_frame = Frame(main_frame)
category_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Category Treeview
category_tree = ttk.Treeview(category_frame)
category_tree.heading("#0", text="Categories")
category_tree.pack(fill="both", expand=True)

# Configure grid weights
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(0, weight=1)

# Refresh the category section
refreshCategorySection()

# Run the application
root.mainloop()