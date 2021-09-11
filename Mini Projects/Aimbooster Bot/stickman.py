# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from PIL.ImageOps import grayscale
from pyautogui import *
import time
import keyboard
import random
import win32api, win32con
import pathlib

while 1:
    # print(locateOnScreen(f"{pathlib.Path(__file__).parent.absolute()}/Stickman.png"))
    if locateOnScreen(f"{pathlib.Path(__file__).parent.absolute()}/stk.png", confidence=.8, region=(0, 0, 1080, 1920), grayscale=True) != None:
        print("here it is")
        time.sleep(0.3)
    else:
        print("NOP!")
        time.sleep(0.3)