from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title('Icon')

root.iconbitmap("src//fruit.ico")
# add icon

img = ImageTk.PhotoImage(Image.open("src\\landscape.jpg").resize((500, 500), Image.ANTIALIAS))
img2 = ImageTk.PhotoImage(Image.open("src\\ball.png").resize((500, 500), Image.ANTIALIAS))
img3 = ImageTk.PhotoImage(Image.open("src\\shoe.png").resize((500, 500), Image.ANTIALIAS))
img4 = ImageTk.PhotoImage(Image.open("src\\soccer.jpeg").resize((500, 500), Image.ANTIALIAS))
img5 = ImageTk.PhotoImage(Image.open("src\\soccer_practice.jpg").resize((500, 500), Image.ANTIALIAS))
# define img

img_list = [img, img2, img3, img4, img5]

status = Label(root, text=f"Image 1 of " + str(len(img_list)), bd=1, relief=SUNKEN, anchor=E)
# anchor --> align to E W N S

label = Label(image=img)
label.grid(row=0, column=0, columnspan=3)


def forward(i):
    global label, button_forward, button_back

    label.grid_forget()
    label = Label(image=img_list[i - 1])

    button_forward = Button(root, text=">>", command=lambda: forward(i + 1))
    button_back = button_back = Button(root, text="<<", command=lambda: back(i - 1))

    if i == len(img_list):
        button_forward = Button(root, text=">>", state=DISABLED)

    label.grid(row=0, column=0, columnspan=3)
    button_back.grid(row=1, column=0)
    button_forward.grid(row=1, column=2)
    # update buttons

    status = Label(root, text=f"Image {str(i)} of {str(len(img_list))}", bd=1, relief=SUNKEN, anchor=E)
    status.grid(row=2, column=0, columnspan=3, sticky=W + E)
    # update status bar


def back(i):
    global label, button_forward, button_back

    label.grid_forget()
    label = Label(image=img_list[i - 1])

    button_forward = Button(root, text=">>", command=lambda: forward(i + 1))
    button_back = button_back = Button(root, text="<<", command=lambda: back(i - 1))

    if i == 1:
        button_back = Button(root, text="<<", state=DISABLED)

    label.grid(row=0, column=0, columnspan=3)
    button_back.grid(row=1, column=0)
    button_forward.grid(row=1, column=2)

    status = Label(root, text=f"Image {str(i)} of {str(len(img_list))}", bd=1, relief=SUNKEN, anchor=E)
    status.grid(row=2, column=0, columnspan=3, sticky=W + E)


button_back = Button(root, text="<<", command=lambda: back)
button_forward = Button(root, text=">>", command=lambda: forward(2))
button_quit = Button(root, text="Quit", command=root.quit)

button_back.grid(row=1, column=0)
button_forward.grid(row=1, column=2)
button_quit.grid(row=1, column=1)
status.grid(row=2, column=0, columnspan=3, sticky=W+E)
# sticky --> stretch from West to East

root.mainloop()
