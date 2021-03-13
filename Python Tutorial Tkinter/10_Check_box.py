from tkinter import *

root = Tk()
root.title('Hi')
root.iconbitmap("src//fruit.ico")
root.geometry("400x400")

var = StringVar()
c = Checkbutton(root, text="How are you?", variable=var, onvalue="Pizza!", offvalue="Jack digs")
# default onvalue is 1, offvalue is 0

c.deselect()
# must do this to avoid the bug
c.pack()


def show():
    Label(root, text=var.get()).pack()


Button(root, text="Show selection", command=show).pack()


mainloop()
