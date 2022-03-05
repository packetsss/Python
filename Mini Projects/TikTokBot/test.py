import win32gui
import datetime
import pandas as pd
import uiautomator2 as u2
from pyvda import AppView, VirtualDesktop
from utils import file_io, followers_quality, restart_android_emulator

# fans_list = file_io("quality_logs/fans.log", mode="r")
# friends_list = file_io("quality_logs/friends.log", mode="r")
# overall_list = file_io("quality_logs/overall.log", mode="r")

# print(len(fans_list) + len(friends_list), len(overall_list))

# d = u2.connect()
# print(d(text="Don't allow").exists)
# d.screenshot(f"screenshots\\{datetime.datetime.now().strftime('%m.%d %H-%M-%S')}.jpg")
# img.save()
def move_window():
    hwnd = win32gui.FindWindow(None, "tiktok")
    AppView(hwnd=hwnd).move(VirtualDesktop(2))

    x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
    w = x1 - x0  # width
    h = y1 - y0  # height
    win32gui.MoveWindow(hwnd, 1043, 40, w, h, True)

move_window()
# followers_quality(d)
