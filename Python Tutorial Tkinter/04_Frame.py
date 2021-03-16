from tkinter import *

root = Tk()
root.title('Frame')
root.iconbitmap("src//fruit.ico")

frame = LabelFrame(root, text="This is my frame...", padx=50, pady=50)
frame.pack(padx=10, pady=10)
# we can do grid inside pack

b = Button(frame, text="Click here to in0sert virus")
b2 = Button(frame, text="Hello?")

b.grid(row=0, column=0)
b2.grid(row=1, column=0)


root.mainloop()
