from tkinter import *

root = Tk()
root.title('Hi')
root.iconbitmap("src//fruit.ico")
root.geometry("400x400")


def clicker(event=None):
    label = Label(root, text="Hlw")
    label.pack()
    pass


btn = Button(root, text="Click", command=clicker)
btn.bind("<Enter>", clicker)
# event, action
btn.pack()


mainloop()
