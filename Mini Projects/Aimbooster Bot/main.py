from PIL.ImageOps import grayscale
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import pathlib
import matplotlib.pyplot as plt

time.sleep(2)
RGB = (255, 219, 195)
last_loc = None
last_loc_x = last_loc_y = [0]

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    # time.sleep(0.001)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    

while not keyboard.is_pressed("q"):
    pic = pyautogui.screenshot(region=(1155, 879, 2649 - 1155, 1927 - 879))
    plt.imshow(pic)
    plt.show()
    break
    w, h = pic.size

    for x in range(0, w, 5):
        for y in range(0, h, 5):
            r, g, b = pic.getpixel((x, y))
            if b == 195:
                loc = (x + 1155, y + 879)
                if loc[0] in last_loc_x and loc[1] in last_loc_y:
                    continue
                else:
                    click(*loc)
                    last_loc_x = range(loc[0] - 15, loc[0] + 15)
                    last_loc_y = range(loc[1] - 15, loc[1] + 15)
                    break
    # print(locateOnScreen(f"{pathlib.Path(__file__).parent.absolute()}/Stickman.png"))
    # if pyautogui.locateOnScreen(f"{pathlib.Path(__file__).parent.absolute()}/stk.png", confidence=.8, region=(441, 170, 1077, 799), grayscale=True) != None:
    #     print("here it is")