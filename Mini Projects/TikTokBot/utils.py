import os
import json
import logging
import adbutils
import win32api
import win32gui
import datetime
import pandas as pd
from time import sleep
import uiautomator2 as u2
from collections import deque
from pyvda import AppView, VirtualDesktop


def start(d: u2.Device) -> bool:
    # close not responding app
    if d(resourceId="android:id/aerr_close").exists:
        d(resourceId="android:id/aerr_close").click()

    # open tiktok
    d.press("home")
    d.press("recent")
    sleep(0.5)
    d.swipe(400, 100, 400, 900, 0.03)
    sleep(0.5)
    d.click(641, 86)
    sleep(0.5)
    d.press("home")
    sleep(0.5)

    # start app
    d.click(97, 550)
    sleep(1)
    # restart if wait too long
    if not d.wait_activity(
        "com.ss.android.ugc.aweme.splash.SplashActivity", timeout=10
    ):
        d.app_stop_all()
        sleep(10)
        d.press("home")
        return False

    return True


def text_to_num(text, bad_data_val=0):
    d = {"K": 1000, "M": 1000000, "B": 1000000000}
    if not isinstance(text, str):
        # Non-strings are bad are missing data in poster's submission
        return bad_data_val

    elif text[-1] in d:
        # separate out the K, M, or B
        num, magnitude = text[:-1], text[-1]
        return int(float(num) * d[magnitude])
    else:
        try:
            return float(text)
        except ValueError as e:
            print(e, "\n", text)
            return 0


def create_logger(name: str) -> logging.Logger:
    r = logging.getLogger("root")
    r.disabled = True

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # create file handler
    fh = logging.FileHandler(f"logs/{name}.log")
    fh.setLevel(logging.DEBUG)
    # create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    logger.info(f"{name.capitalize()} bot initialized...")

    return logger


def file_io(filename, mode="r", lst=None):
    if mode == "r":
        with open(filename, "r") as f:
            lst = json.load(f)
            if not lst:
                return []
        return lst

    if mode == "w":
        with open(filename, "w") as f:
            json.dump(lst, f)


def followers_quality(d):
    def get_name(xx):
        return (
            xx.sibling(className="android.widget.LinearLayout")
            .child(resourceId="com.zhiliaoapp.musically:id/fs9")
            .info["text"]
        )

    sleep(0.3)
    d(resourceId="com.zhiliaoapp.musically:id/be6").click()
    sleep(3)

    ct = 0
    total_ct = 0
    fans_list = []
    friends_list = []
    overall_list = []

    last_username_queue = deque(maxlen=3)

    while 1:
        # log info into lists
        try:
            ct += 1
            for x in d(resourceId="com.zhiliaoapp.musically:id/e5q"):
                total_ct += 1
                last_element = x
                username = get_name(x)
                if username in overall_list:

                    continue

                overall_list.append(username)
                if (
                    x.child(resourceId="com.zhiliaoapp.musically:id/frq").info["text"]
                    == "Friends"
                ):
                    friends_list.append(username)
                else:
                    fans_list.append(username)

            # if reach to the end
            last_username_queue.append(username)
            if len(last_username_queue) == 3 and len(set(last_username_queue)) == 1:
                file_io("quality_logs/fans.log", mode="w", lst=fans_list)
                file_io("quality_logs/friends.log", mode="w", lst=friends_list)
                file_io("quality_logs/overall.log", mode="w", lst=overall_list)
                return f"{len(friends_list)}/{len(fans_list)}: {round(len(fans_list) / len(overall_list), 3) * 100}%"

            if username in overall_list:
                time = (last_element.info["bounds"]["bottom"] - 210) / 6500
                d.swipe(350, last_element.info["bounds"]["bottom"] - 50, 350, 380, time)

            if ct % 50 == 0:
                print(f"Total viewed: {total_ct}")

        except u2.exceptions.UiObjectNotFoundError:
            pass
        except Exception as e:
            print(e)


def tracking_data(d: u2.Device, logger: logging.Logger) -> pd.DataFrame:
    def format_plus_minus(num, idx):
        rst = int(num - float(df.iloc[-1, idx].split("(")[0]))
        return str(rst) if rst <= 0 else f"+{rst}"

    df = pd.read_csv("tracking.csv", index_col=0)

    date_comp = list(map(lambda x: int(x), df.iloc[-1].date.split("-")))

    # new day update
    if datetime.date(*date_comp) < datetime.date.today():
        while not start(d):
            logger.warning("TikTok started failed, retrying...")
        sleep(0.5)
        d.click(633, 1200)
        sleep(0.5)
        following = text_to_num(
            d(resourceId="com.zhiliaoapp.musically:id/beg").info["text"]
        )
        followers = text_to_num(
            d(resourceId="com.zhiliaoapp.musically:id/be6").info["text"]
        )
        likes = text_to_num(
            d(resourceId="com.zhiliaoapp.musically:id/ar0").info["text"]
        )

        data = {
            "date": [datetime.date.today()],
            "total following": [
                f"{int(following)} ({format_plus_minus(following, 1)})"
            ],
            "total followers": [
                f"{int(followers)} ({format_plus_minus(followers, 2)})"
            ],
            "total likes": [f"{int(likes)} ({format_plus_minus(likes, 3)})"],
            "followed": [0],
            "unfollowed": [0],
            "friends/fans": [None],
            # "friends/fans": [followers_quality(d)],
        }

        df = df.append(pd.DataFrame(data))
        df.to_csv("tracking.csv")

    return df


def update_count(name: str, view_only: bool = False):
    df = pd.read_csv("tracking.csv", index_col=0)
    if any(str(datetime.date.today()) == df.date):
        if not view_only:
            df.loc[df.date == str(datetime.date.today()), name] += 1
            df.to_csv("tracking.csv")
    else:
        return None

    return int(df.loc[df.date == str(datetime.date.today()), name])


def move_window(desktop_number=2):
    hwnd = win32gui.FindWindow(None, "tiktok")
    AppView(hwnd=hwnd).move(VirtualDesktop(desktop_number))

    x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
    w = x1 - x0  # width
    h = y1 - y0  # height
    win32gui.MoveWindow(hwnd, 1043, 40, w, h, True)


def restart_android_emulator():
    while 1:
        os.system("taskkill /f /im dnplayer.exe")
        win32api.WinExec("D:/LDPlayer/LDPlayer4.0/dnplayer.exe")
        print("Emulator has been restarted")
        sleep(1)
        move_window()
        sleep(7)
        connect_ct = 0
        while 1:
            if connect_ct > 10:
                break
            try:
                adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
                d = adb.device()
                os.system("adb devices")
                u2.connect()
                return
            except Exception as e:
                connect_ct += 1
                print(e)
                sleep(1)
                continue


if __name__ == "__main__":
    # adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    # d = adb.device()
    # os.system("adb devices")
    # d.click(100, 100)
    restart_android_emulator()
