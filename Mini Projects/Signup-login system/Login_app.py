# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

try:
    import tkinter as tk  # python 3
    from tkinter import font as tkfont
    from tkinter import *  # python 3
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2
import Login_signup


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Paul's login system", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Sign up",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Login",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()


class PageOne(tk.Frame):

    def signup(self):
        user_name = self.user_entry.get()
        print(user_name)
        with open("User_data.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                while re.search(f"Username: {user_name};", line):
                    print("Username already taken, try a new one.")
                    user_name = input("Type in a new username: ")

        password = input("Type in a new password: ")

        with open("User_data.txt", "a") as f:
            f.writelines("Username: " + user_name + ";\nPassword: " + password + ".\n\n")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        user_text = StringVar()
        user_label = Label(self, font="bold, 9", text="Please type in your username:", pady=5)
        user_label.pack()
        self.user_entry = Entry(self, textvariable=user_text, width=28)
        self.user_entry.pack()

        password_text = StringVar()
        password_label = Label(self, font="bold, 9", text="Please type in your username:", pady=5)
        password_label.pack()
        password_entry = Entry(self, textvariable=password_text, width=28)
        password_entry.pack()

        # label = tk.Label(self, text="This is page 1", font=controller.title_font)
        # label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Sign up", command=self.signup())
        button.pack()




class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
