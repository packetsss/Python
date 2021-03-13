from tkinter import *

root = Tk()
root.title("Calculator")
# change title

e = Entry(root, width=35, borderwidth=2)
e.grid(row=0, column=0, columnspan=30, padx=10, pady=10)

fst_number, math = None, None


def add_():
    global fst_number, math
    fst_number, math = int(e.get()), "add"
    e.delete(0, END)
    pass


def subtract():
    global fst_number, math
    fst_number, math = int(e.get()), "sub"
    e.delete(0, END)
    pass


def multiply():
    global fst_number, math
    fst_number, math = int(e.get()), "mul"
    e.delete(0, END)
    pass


def divide():
    global fst_number, math
    fst_number, math = int(e.get()), "div"
    e.delete(0, END)
    pass


def equal():
    snd_number = int(e.get())
    e.delete(0, END)
    if math == "add":
        rst = fst_number + snd_number
    elif math == "sub":
        rst = fst_number - snd_number
    elif math == "mul":
        rst = fst_number * snd_number
    elif math == "div":
        rst = fst_number / snd_number

    e.insert(0, rst)


def clear():
    e.delete(0, END)


def click(number):
    current = e.get()
    e.delete(0, END)
    new = str(current) + str(number)
    e.insert(0, new)


button_list = []
for i in range(0, 10):
    button = Button(root, text=str(i), padx=40, pady=20, command=lambda i=i: click(i))
    button_list.append(button)

for i, button in enumerate(button_list):
    if i == 0:
        button.grid(row=4, column=0)
        continue
    button.grid(row=4 - (i + 2) // 3, column=(i + 2) % 3)

button_add = Button(root, text="+", padx=39, pady=20, command=add_)
button_add.grid(row=5, column=0)

button_subtract = Button(root, text="-", padx=41, pady=20, command=subtract)
button_subtract.grid(row=6, column=0)

button_multiply = Button(root, text="*", padx=42, pady=20, command=multiply)
button_multiply.grid(row=6, column=1)

button_divide = Button(root, text="/", padx=42, pady=20, command=divide)
button_divide.grid(row=6, column=2)

button_equal = Button(root, text="=", padx=90, pady=20, command=equal)
button_equal.grid(row=5, column=1, columnspan=2)

button_clear = Button(root, text="Clear", padx=79, pady=20, command=clear)
button_clear.grid(row=4, column=1, columnspan=2)

root.mainloop()
