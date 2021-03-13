from tkinter import *

root = Tk()
root.title('Hi')
root.iconbitmap("src//fruit.ico")
root.geometry("400x400")


def show():
    Label(root, text=click.get()).pack()


options = ["M", "Tu", "W", "Th", "F", "Sa", "Su"]

click = StringVar()
click.set("M")
drop = OptionMenu(root, click, *options)
# put * before list
drop.pack()

Button(root, text="Show selection", command=show).pack()

mainloop()