# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from tkinter import *

root = Tk()
root.title('Frame')
root.iconbitmap("src//fruit.ico")

modes = [
    ("Pepperoni", "Pepperoni"),
    ("Cheese", "Cheese"),
    ("Mushroom", "Mushroom"),
    ("Onion", "Onion")]

pizza = StringVar()
pizza.set("Pepperoni")

for text, toppings in modes:
    # use a for loop to create multiple radio buttons

    Radiobutton(root, text=text, variable=pizza, value=toppings).pack()
    # variable type must match value type
    # variable is start option


def click(value):

    label1 = Label(root, text=value)
    label1.pack()


bn = Button(root, text="hlw", command=lambda: click(pizza.get()))
bn.pack()

root.mainloop()
