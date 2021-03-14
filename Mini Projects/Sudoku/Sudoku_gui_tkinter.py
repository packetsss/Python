from tkinter import *
from Sudoku_interface import interface
from Sudoku_solver import solve
import numpy as np
from tkinter import messagebox
from PIL import ImageTk, Image
from copy import deepcopy


class create_button:
    def __init__(self, frame, x, y, root, number, board, canvas, i, j, ct):
        self.frame = frame
        self.root = root
        self.canvas = canvas
        self.number = number
        self.board = board

        self.x = x
        self.y = y
        self.i = i
        self.j = j
        self.ct = ct

        self.bt = Button(self.frame, bd=0, command=self.input,
                         text=number, relief=SUNKEN, font=("Helvetica", 30), bg="white")

    def change_button(self, button):
        self.bt = button

    def get_position(self):
        return self.i, self.j

    def get_button(self):
        return self.bt

    def get_counter(self):
        return self.ct

    def draw_button(self):
        self.bt.bind("<Enter>", lambda _: self.bt.configure(bg="light yellow"))
        self.bt.bind("<Leave>", lambda _: self.bt.configure(bg="white"))
        self.bt.pack(expand=1, fill=BOTH)

    def draw_fixed_button(self):
        self.bt.configure(command=NONE, bg="#9ED9CC", activebackground="#9ED9CC")

        self.bt.pack(expand=1, fill=BOTH)

    def draw_hint_button(self):
        bt = Button(self.frame, bd=0, text=self.number, relief=SUNKEN,
                    font=("Helvetica", 30), bg="#FFDDE2", activebackground="#FFDDE2")
        bt.pack(expand=1, fill=BOTH)

    def input(self):

        def onKeyPress(event=None):
            inputs = event.char
            if inputs in "123456789":
                inputs = int(event.char)
                if solve(self.board).check_v2(self.x, self.y, inputs):
                    self.bt.configure(text=inputs, bg="white")
                    self.board[self.x, self.y] = inputs

                    self.bt.bind("<Enter>", lambda _: self.bt.configure(bg="light yellow"))
                    self.bt.bind("<Leave>", lambda _: self.bt.configure(bg="white"))
                    self.root.unbind('<KeyPress>')
                else:
                    messagebox.showwarning("Existing Warning", "This number already exists, please try another one")
            else:
                messagebox.showerror("Input Error", "Error: Invalid input")

        self.board[self.x, self.y] = 0
        self.bt.configure(text='', bg="#AF814D")

        self.bt.unbind("<Enter>")
        self.bt.unbind("<Leave>")
        self.root.bind('<KeyPress>', onKeyPress)


def create_button_list(dim, canvas, root, board):
    frames_list = []
    canvas_id = []
    ct = 0
    width = dim // 9 - 8

    btn_list = []

    for x, i in enumerate(range(4, dim - (dim // 9), dim // 9)):
        btn_list.append([])
        for y, j in enumerate(range(4, dim - (dim // 9), dim // 9)):
            frames_list.append(Frame(root, width=width, height=width, bg="#FFDDE2"))
            frames_list[ct].propagate(False)

            num = str(board[x, y]) if board[x, y] != 0 else ''
            if num == '':
                # if num = 0, create input able button
                btn_list[x].append(create_button(frames_list[ct], x, y, root, num, board, canvas, i, j, ct))
                btn_list[x][y].draw_button()
            else:
                # if num != 0, create fixed button
                btn_list[x].append(create_button(frames_list[ct], x, y, root, num, board, canvas, i, j, ct))
                btn_list[x][y].draw_fixed_button()
            canvas_id.append(canvas.create_window(j + 5, i + 5, anchor="nw", window=frames_list[ct]))

            ct += 1
            # ct to keep track of frame list

    return btn_list


def func_buttons(canvas1, root, back_up, board, b_lst):
    def reset(prompt=True, shuffle=False):
        def change_event(e):
            nonlocal i, j
            b_lst[i][j].get_button().configure(bg="light yellow")

        cond = False
        if prompt:
            cond = messagebox.askokcancel("Prompt reset", "Are you sure to reset the puzzle? You will lose everything!")
        if cond or not prompt:
            nonlocal board, back_up_prev, back_up
            if shuffle:
                back_up = np.array(interface(random=True).foundation())
                print(back_up)
            board = deepcopy(back_up)
            back_up_prev = deepcopy(back_up)

            hint_bt.configure(command=lambda: hint(ai_activated=False))

            ai_btn.destroy()
            for i in range(9):
                for j in range(9):
                    num = str(board[i, j]) if board[i, j] != 0 else ''
                    if not num:
                        b_lst[i][j].get_button().configure(text="", bg="white",
                                                           command=b_lst[i][j].input)

                        b_lst[i][j].get_button().bind("<Enter>", lambda _, x=i, y=j: b_lst[x][y].get_button()
                                                      .configure(bg="light yellow"))
                        b_lst[i][j].get_button().bind("<Leave>", lambda _, x=i, y=j: b_lst[x][y].get_button()
                                                      .configure(bg="white"))
                    else:
                        b_lst[i][j].get_button().configure(command=NONE, text=num, bg="#9ED9CC",
                                                           activebackground="#9ED9CC")
                        b_lst[i][j].get_button().unbind("<Enter>")
                        b_lst[i][j].get_button().unbind("<Leave>")

    def hint(ai_activated=False):
        nonlocal board, back_up_prev
        ai_back_up_prev = deepcopy(back_up_prev)
        if ai_activated:
            if not solve(back_up_prev).init(back_up_prev) or not solve(back_up_prev).unique(back_up_prev) \
                    or not solve(back_up_prev).elimination(back_up_prev):
                messagebox.showerror("Puzzle solving error",
                                     "Sorry, error occurred during solving, resetting the puzzle...")
                reset(prompt=False)
                return None
            else:
                # update the buttons
                for i in range(9):
                    for j in range(9):
                        if len(str(back_up_prev[i, j])) > 1:
                            back_up_prev[i, j] = 0
                        elif back_up_prev[i, j] != 0 and ai_back_up_prev[i, j] != back_up_prev[i, j]:
                            b_lst[i][j].get_button().configure(text=back_up_prev[i, j], command=NONE
                                                               , bg="#FFDDE2", activebackground="#FFDDE2")
                            b_lst[i][j].get_button().unbind("<Enter>")
                            b_lst[i][j].get_button().unbind("<Leave>")
                if np.array_equal(ai_back_up_prev, back_up_prev):
                    messagebox.showinfo("No hints available", "Sorry, the current method can't give you any hint")

        else:
            if not solve(board).init(board) or not solve(board).unique(board) \
                    or not solve(board).elimination(board):
                messagebox.showerror("Puzzle solving error",
                                     "Sorry, error occurred during solving, resetting the puzzle...")
                reset(prompt=False)
                return None
            for i in range(9):
                for j in range(9):
                    if len(str(board[i, j])) > 1:
                        board[i, j] = 0
                    elif board[i, j] != 0 and board[i, j] != back_up_prev[i, j]:
                        # delete the orig canvas and create a new one
                        # i * 9 + j + 2 --> canvas id
                        # i * 9 + j --> canvas_list index & frame_list index

                        b_lst[i][j].get_button().configure(text=board[i, j], command=NONE
                                                           , bg="#FFDDE2", activebackground="#FFDDE2")
                        b_lst[i][j].get_button().unbind("<Enter>")
                        b_lst[i][j].get_button().unbind("<Leave>")

            if np.array_equal(board, back_up_prev):
                ans = messagebox.askyesno("No hints available", "Sorry, the current method can't give you even one "
                                                                "more hint! Do you want to enable super AI mode?")
                if ans:
                    ai_mode()
                    return None
            else:
                back_up_prev = deepcopy(board)

    def shuffle():
        ans = messagebox.askyesno("Shuffle puzzle", "Are you sure to shuffle the puzzle? "
                                                    "You will lose everything in this board!")
        if ans:
            reset(shuffle=True, prompt=False)

    def ai_mode():
        nonlocal board, hint_bt, back_up_prev, ai_btn
        ai_btn = Button(root, bd=0, command=ai_hint, text="Get a hint\nfrom SUPER AI", font=("Poplar Std", 15),
                        bg="#EEA47F", width=14, fg="#00539C")
        canvas1.create_window(20, 600, anchor="nw", window=ai_btn)

        back_up_prev = deepcopy(board)

        board, _, _ = solve(board).ai()
        hint_bt.configure(command=lambda: hint(ai_activated=True))

    def ai_hint():
        nonlocal back_up_prev
        i, j = np.random.randint(1, 9), np.random.randint(1, 9)

        while back_up_prev[i, j] != 0:
            i, j = np.random.randint(1, 9), np.random.randint(1, 9)
        back_up_prev[i, j] = board[i, j]

        b_lst[i][j].get_button().configure(text=board[i, j], command=NONE
                                           , bg="#EEA47F", activebackground="#EEA47F")
        b_lst[i][j].get_button().unbind("<Enter>")
        b_lst[i][j].get_button().unbind("<Leave>")

    # Buttons
    back_up_prev = deepcopy(back_up)

    reset_bt = Button(root, bd=0, command=reset, text="Reset puzzle", font=("Poplar Std", 15), bg="#041E42",
                      width=14, fg="#AFEADC")
    hint_bt = Button(root, bd=0, command=hint, text="Calculate hints\nusing AI", font=("Poplar Std", 15), fg="#00539C",
                     width=14, bg="#EEA47F")
    shuffle_bt = Button(root, bd=0, command=shuffle, text="Shuffle puzzle", font=("Poplar Std", 15), bg="#EEA47F",
                        width=14, fg="#00539C")
    ai_btn = Button(root, bd=0, command=ai_hint, text="Get a hint\nfrom SUPER AI", font=("Poplar Std", 15),
                    bg="#EEA47F", width=14, fg="#00539C")

    canvas1.create_window(20, 700, anchor="nw", window=reset_bt)
    canvas1.create_window(20, 50, anchor="nw", window=hint_bt)
    canvas1.create_window(20, 150, anchor="nw", window=shuffle_bt)


def main():
    board = np.array(interface(random=False).foundation())
    backup_board = deepcopy(board)

    root = Tk()
    root.title('The Sudokuer')
    root.configure(bg="light gray")
    img = PhotoImage(file='src\\icon.gif')
    root.tk.call('wm', 'iconphoto', root._w, img)

    dimension = 800
    root.geometry(str(dimension + 250) + "x" + str(dimension) + "+350-120")

    c = Canvas(root, height=dimension, width=dimension, bg="black", bd=0, highlightthickness=0)
    img_bg = ImageTk.PhotoImage(Image.open("src\\Board_background.jpg").resize((dimension, dimension), Image.ANTIALIAS))
    c.create_image(0, 0, image=img_bg, anchor=NW)
    b_lst = create_button_list(dimension, c, root, board)
    c.grid(row=0, column=0)

    c1 = Canvas(root, height=dimension, width=250, bg="light gray", bd=0, highlightthickness=0)
    c1.grid(row=0, column=1)
    func_buttons(c1, root, backup_board, board, b_lst)

    root.mainloop()


if __name__ == "__main__":
    main()
