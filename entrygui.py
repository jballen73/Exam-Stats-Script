import tkinter as tk
number = None
root = None
button = None
text_row = 1
def run():
    global root
    root = tk.Tk()
    num_label = tk.Label(root, text="Number of Questions")
    num_label.grid(sticky=tk.W)
    global number, text_row, button
    number = tk.StringVar(root)
    num_field = tk.Entry(root, textvariable=number)
    num_field.grid(row=0, column=1, sticky=tk.E)
    button = tk.Button(root, text="Print", command=add_line)

    button.grid(sticky=tk.W+tk.E+tk.S)
    root.mainloop()

def print_number():
    value = int(number.get())
    print(value)
    print(type(value))

def add_line():
    global text_row
    label = tk.Label(root, text="New Line")
    label.grid(row=text_row, sticky=tk.W)
    text_row += 1
    button.grid(row=text_row, sticky=tk.W+tk.E+tk.S)