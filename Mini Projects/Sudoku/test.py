from tkinter import *

root = Tk()
frames_list = []
btn_list = []
turn = "X"


def process_turn(ndex):
    if btn_list[ndex]["text"] == turn:
        btn_list[ndex].config(text=116)
    else:
        btn_list[ndex].config(text=turn)


def create_frames_and_buttons():
    ndex = 0
    i = 0
    x = 0
    for i in range(3):
        for x in range(3):
            frames_list.append(Frame(root, width=100, height=100))
            frames_list[ndex].propagate(False)
            frames_list[ndex].grid(row=i, column=x, sticky="nsew", padx=2, pady=2)

            btn_list.append(Button(frames_list[ndex], command=lambda x=ndex: process_turn(x)))
            btn_list[ndex].pack(expand=True, fill=BOTH)
            x += 1
            ndex += 1
        i += 1
    root.resizable(width=False, height=False)
    print(frames_list)


create_frames_and_buttons()
mainloop()
