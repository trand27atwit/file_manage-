from tkinter import *
from tkinter import ttk  # Import ttk for Combobox

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

    # Category Label
    category_label = Label(c_window, text="Category:")
    category_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

   
    # Create button
    create_button = Button(c_window, text="Create", command=c_window.destroy)
    create_button.grid(row=3, column=1, columnspan=2, pady=10)

# Function to open the "New SubCategory" window
def subcategoryWin():
    sub_window = Toplevel(root)
    sub_window.title('New SubCategory')
    sub_window.geometry('400x300')

    # Category Label
    subc_label = Label(sub_window, text="Category:")
    subc_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Dropdown for Category Selection
    categories = ["Food", "Electronics", "Clothing", "Books"]  # Example categories
    subc_dropdown = ttk.Combobox(sub_window, values=categories, state="readonly", width=27)
    subc_dropdown.grid(row=0, column=1, padx=10, pady=10)
    subc_dropdown.current(0)  # Set default selection

    # Name label
    subname_label = Label(sub_window, text="Subcategory Name:")
    subname_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    # Name entry field
    subname_entry = Entry(sub_window, width=30)
    subname_entry.grid(row=1, column=1, padx=10, pady=10)

# Root window
root = Tk()
root.title('Easy Find')
root.geometry('600x400')

# Create the menu bar
menubar = Menu(root)
root.config(menu=menubar)

# Create the "New" menu
new_menu = Menu(menubar, tearoff=0)
new_menu.add_command(label='New Category', command=categoryWin)
new_menu.add_command(label='New Subcategory', command=subcategoryWin)
menubar.add_cascade(label='New', menu=new_menu)  # Attach the new menu

# Create the "Modify" menu
modify_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Modify', menu=modify_menu)

# Create the "Delete" menu
delete_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Delete', menu=delete_menu)

# Run the application
root.mainloop()
