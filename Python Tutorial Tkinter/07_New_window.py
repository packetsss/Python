# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title('Hi')
root.iconbitmap("src//fruit.ico")

img = ImageTk.PhotoImage(Image.open("src\\landscape.jpg").resize((500, 500), Image.ANTIALIAS))
# image needs to be global

def open():
    top = Toplevel()
    # new window

    top.title("Snd window")

    Label(top, text="Hlw World!").pack()
    Label(top, image=img).pack()
    Button(top, text="Close window", command=top.destroy).pack()
    # close window


btn = Button(root, text="Open new window", command=open).pack()


mainloop()
