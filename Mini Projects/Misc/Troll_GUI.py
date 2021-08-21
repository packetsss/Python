from tkinter import *


def Me():
    my_list.insert(END, "Okie\n欧克")


def You():
    my_list.insert(END, "I don't like you!你坏坏?!!")


def Lmj():
    my_list.insert(END, f"我是{my_text.get()}, 你是{your_text.get()}的老母鸡!!咯咯咯！！")


def sign_up():
    root.destroy()
    s = Tk()
    s.title("Sign up")
    s.geometry("700x350")


root = Tk()
root.title("User End Login System")
root.geometry("700x350")

signup_button = Button(root, text="Sign up", width=8, command=sign_up)
signup_button.grid(row=0, column=0, pady=20)

login_button = Button(root, text="Login", width=8, command=Me)
login_button.grid(row=0, column=1, pady=20)

my_text = StringVar()
my_label = Label(root, font="bold", text="I am(我是):", pady=15)
my_label.grid(row=0, column=0, sticky=W)
my_entry = Entry(root, textvariable=my_text)
my_entry.grid(row=0, column=1)

your_text = StringVar()
your_label = Label(root, font="bold", text="You are(你是):", padx=20, pady=15)
your_label.grid(row=0, column=2, sticky=W)
your_entry = Entry(root, textvariable=your_text)
your_entry.grid(row=0, column=3)

my_list = Listbox(root, height=8, width=50, border=0)
my_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20)

scrollbar = Scrollbar(root)
scrollbar.grid(row=3, column=3)

my_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=my_list.yview)

me_button = Button(root, text="Hi!", width=8, command=Me)
me_button.grid(row=1, column=0, pady=20)

you_button = Button(root, text="Yo! DON'T you dare to click me\n你敢点我?!", width=30, command=You)
you_button.grid(row=1, column=2, padx=0, pady=0)

lmj_button = Button(root, text="老母鸡", width=10, command=Lmj)
lmj_button.grid(row=2, column=0, padx=0, pady=0)

root.mainloop()

