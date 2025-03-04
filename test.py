from tkinter import *

# create root window
root = Tk()
menu= Menu(root)
root.config(menu=menu)
newmenu=Menu(menu)
# the new button section
menu.add_cascade(label='New', menu=newmenu)
newmenu.add_command(label='New Category')
newmenu.add_command(label='New Subcategory')

# the modification button
menu.add_cascade(label='Modify',menu=newmenu )

# the delete button
menu.add_cascade(label='Delete', menu=newmenu)


# Execute Tkinter
mainloop()