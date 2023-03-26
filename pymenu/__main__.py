import tkinter as tk
from tkinter.ttk import *

input_list = """
apple
banana
cherry
date
elderberry
""".split()


def update_listbox(event):
    # Clear the Listbox
    listbox.delete(0, tk.END)

    # Get the current text in the Entry widget
    text = entry.get()

    # Loop through the dummy data and add matching items to the Listbox
    for item in input_list:
        if text.lower() in item.lower():
            listbox.insert(tk.END, item)
            
    # select the first item
    listbox.select_set(0)

root = tk.Tk()

font = ('Arial', 32)

# Create an Entry widget for user input
entry = tk.Entry(root, font=font)
entry.pack()

# Create a Listbox widget to display suggestions
listbox = tk.Listbox(root, font=font)
listbox.pack()

# Bind the Entry widget to a function that updates the Listbox
entry.bind('<KeyRelease>', update_listbox)
entry.focus_set()

# Add some dummy data to the Listbox
for elem in input_list:
    listbox.insert(tk.END, elem)

listbox.select_set(0)

# override_redirect=True makes the window borderless
root.overrideredirect(True)

# Get the requested size of the window
req_width = root.winfo_reqwidth()
req_height = root.winfo_reqheight()

# Get the screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the coordinates of the top-left corner of the window
x = (screen_width - req_width) // 2
y = (screen_height - req_height) // 2

# Move the window to the center of the screen
root.geometry(f"+{x}+{y}")

root.tk.call('tk', 'scaling', 2.0)

root.bind('<Escape>', lambda e: root.destroy())
root.bind('<Return>', lambda e: root.destroy())

root.protocol("WM_DELETE_WINDOW", root.destroy)

root.mainloop()
