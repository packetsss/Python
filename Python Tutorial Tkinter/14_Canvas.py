from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title('Hi')
root.iconbitmap("src//fruit.ico")
root.geometry("700x700")

img = ImageTk.PhotoImage(Image.open("src\\landscape.jpg").resize((560, 560), Image.ANTIALIAS))


c = Canvas(root, height=550, width=550, bg="gray", bd=5, highlightthickness=0)
# boarder and high light thickness

c.create_image(0, 0, image=img, anchor="nw")

c.create_line(5, 100, 300, 100, width=5)
# line: (start_x, start_y, end_x, end_y)

c.create_oval(20, 20, 100, 100, outline="green", fill="yellow")
# create oval

c.create_arc(10, 150, 250, 300, extent=150, fill="red")
# arc: (start_x, start_y, end_x, end_y), extent: degree

c.create_rectangle(100, 250, 200, 330)
# add rect


def entry_clear(e):
    entry_box.delete(0, END)
    entry_box.configure(show="*")


entry_box = Entry(root, font=("Helvetica", 20), width=20)
entry_box.insert(0, "Entry")
entry_box.bind("<Button-1>", entry_clear)
window = c.create_window(100, 350, anchor="nw", window=entry_box)
# add the entry box

bt = Button(root, text="Hi", font=("Helvetica", 20), width=19, fg="gray")
window1 = c.create_window(100, 400, anchor="nw", window=bt)
c.pack()



mainloop()
