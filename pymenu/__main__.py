import re
import win32clipboard

import tkinter as tk
from tkinter.ttk import *

input_list = """
apple
banana
cherry
date
elderberry
""".split()


def paste(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text)
    win32clipboard.CloseClipboard()


def update_listbox(event):
    if not event is None:
        if event.state:
            return
        if event.keysym in ['Up', 'Down', 'Control_L']:
            return

    text = entry.get()

    if text == '':
        listbox.delete(0, tk.END)
        for item in input_list:
            listbox.insert(tk.END, item)
        listbox.select_set(0)
        return


    xr = eval_expr(text)
    results = filter(input_list, text)

    if not xr is None or results:
        listbox.delete(0, tk.END)

    if not xr is None:
        listbox.insert(tk.END, xr)

    if results:
        for item in results:
            listbox.insert(tk.END, item)

    listbox.select_set(0)


def filter(input_list, text):
    results = []

    needle = '.*'.join(text)

    try:
        pattern = re.compile(needle, re.IGNORECASE)
    except:
        return []

    for item in input_list:
        if pattern.search(item):
            results.append(item)

    return results


def eval_expr(x):
    try:
        result = eval(x)
    except:
        result = None

    return result


def handle_return(event):
    index = listbox.curselection()
    value = listbox.get(index)
    paste(value)
    root.destroy()


def select_next(event):
    current = listbox.curselection()
    if current:
        next = current[-1] + 1
        if next >= listbox.size():
            next = listbox.size() - 1
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(next)
        listbox.activate(next)


def select_previous(event):
    current = listbox.curselection()
    if current:
        previous = current[0] - 1
        if previous < 0:
            previous = 0
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(previous)
        listbox.activate(previous)


def delete_line(event):
    entry.delete(0, tk.END)


def handle_click(event):
    index = listbox.nearest(event.y)
    item = listbox.get(index)
    paste(item)
    root.destroy()

root = tk.Tk()

font = ('Arial', 50)

# Create an Entry widget for user input
entry = tk.Entry(root, font=font)
entry.pack()

# Create a Listbox widget to display suggestions
listbox = tk.Listbox(root, font=font)
listbox.pack()

# Bind the Entry widget to a function that updates the Listbox
entry.bind('<KeyRelease>', update_listbox)
entry.focus_set()

update_listbox(None)

# override_redirect=True makes the window borderless
root.overrideredirect(True)

root.update()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry("+{}+{}".format(x, y))

root.bind('<Escape>', lambda e: root.destroy())
root.bind('<Return>', handle_return)
root.bind('<FocusOut>', lambda e: root.destroy())
root.bind('<Up>', select_previous)
root.bind('<Down>', select_next)
root.bind('<Control-p>', select_previous)
root.bind('<Control-n>', select_next)
root.bind('<Control-u>', delete_line)

listbox.bind('<Button-1>', handle_click)
root.protocol("WM_DELETE_WINDOW", root.destroy)

root.mainloop()

