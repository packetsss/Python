from tkinter import *

root = Tk()

e = Entry(root, width=50, fg="green", borderwidth=5)
# create a text box
e.pack()

e.insert(0, "Enter your name: ")
# put default text inside the box


def click():
    my_label = Label(root, text=f"Hello {e.get()}!")
    # label is text
    my_label.pack()
    # pack or grid to screen


my_button = Button(root, text="Enter your name", pady=40, padx=50, command=click, fg="magenta", bg="white")
# root, pad_x, pad_y --> size, DON'T need parenthesis for calling command functions
# fg --> foreground color, bg --> background color, can also use hash codes

my_button.pack()
# pack or grid to screen

root.mainloop()
