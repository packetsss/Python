from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

root = Tk()
root.title('Hi')
root.iconbitmap("src//fruit.ico")


def open():
    global img
    root.filename = filedialog.askopenfilename(initialdir="src", title="Select A File",
                                               filetypes=(("png files", "*.png"), ("all files", "*.*")))
    # pop up a window to prompt open a file, returns the location

    Label(root, text=root.filename).pack()
    img = ImageTk.PhotoImage(Image.open(root.filename).resize((500, 500), Image.ANTIALIAS))
    Label(root, image=img).pack()


btn = Button(root, text="Open File", command=open).pack()


mainloop()