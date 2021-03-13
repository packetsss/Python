from tkinter import *

root = Tk()
root.title('Hi')
root.iconbitmap("src//fruit.ico")

root.geometry("400x400")
# change window size


def slide_h(a=None):
    Label(root, text=horizontal.get()).pack()
    root.geometry(f"{str(horizontal.get())}x{str(vertical.get())}")
    # change window size


vertical = Scale(root, from_=0, to=1000)
# need _ for from
vertical.pack()
# need to pack separately

horizontal = Scale(root, from_=0, to=1000, orient="horizontal")
# need to pass in a dummy variable in command
horizontal.pack()


Button(root, text="Click!", command=slide_h).pack()

mainloop()
