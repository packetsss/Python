from tkinter import *
from tkinter import messagebox

root = Tk()
root.title('Icon')
root.iconbitmap("src//fruit.ico")


def pop_up():
    response = messagebox.askquestion("This is Popup!", "Hlw World!")
    # 弹窗
    # types: showinfo, showwarning, showerror, askquestion, askokcancel, askyesno

    #Label(root, text=response).pack()
    if response == 1 or response == "yes":
        Label(root, text="Yes!").pack()
    else:
        Label(root, text="No!").pack()
    # determine what it returns


Button(root, text="PopUp", command=pop_up).pack()


mainloop()
