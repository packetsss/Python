from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title('Hi')
root.iconbitmap("src//fruit.ico")
root.geometry("400x400")

menu = Menu(root)
root.configure(menu=menu)


def new():
    hide_frame()
    file_new_frame.pack(fill="both", expand=1)
    Label(file_new_frame, text="New!").pack()


def cut():
    hide_frame()
    edit_cut_frame.pack(fill="both", expand=1)
    edit_cut_frame.pack(fill="both", expand=1)
    Label(edit_cut_frame, text="Cut!").pack()

def hide_frame():
    file_new_frame.pack_forget()
    edit_cut_frame.pack_forget()


def copy():
    pass


file_menu = Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
# file sub menu
file_menu.add_command(label="New...", command=new)
file_menu.add_separator()
file_menu.add_command(label="Quit", command=root.quit)

edit_menu = Menu(menu)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_separator()
edit_menu.add_command(label="Copy", command=copy)

option_menu = Menu(menu)
menu.add_cascade(label="Option", menu=option_menu)
option_menu.add_command(label="Find", command=copy)
option_menu.add_separator()
option_menu.add_command(label="Find_next", command=copy)

file_new_frame = Frame(root, width=400, height=400, bg="red")
edit_cut_frame = Frame(root, width=400, height=400, bg="blue")


mainloop()
