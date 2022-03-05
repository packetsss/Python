import random
from time import sleep
import uiautomator2 as u2

from utils import *
from config import *
from switch_helper import SwitchHelper


def unfollow_start(d: u2.Device, logger: logging.Logger) -> None:
    from utils import start

    while not start(d):
        logger.warning("TikTok started failed, retrying...")

    # open following page
    sleep(1)
    d.click(633, 1200)
    sleep(2)

    # don't sync facebook popup
    if d(text="Don't allow").exists:
        d(text="Don't allow").click()

    d.click(160, 480)
    sleep(2)

    # scroll down to avoid new following
    scroll_number = random.randint(13, 120)
    print(f"{scroll_number = }")
    for _ in range(scroll_number):
        d.swipe(400, 1100, 400, 200, 0.02)
        sleep(random.uniform(1, 3.5))

    sleep(0.5)


def unfollow(d: u2.Device, logger: logging.Logger, passive: bool = False) -> None:
    try:
        if passive:
            switch_h = SwitchHelper(
                d,
                logger,
                passive=passive,
            )
        else:
            switch_h = SwitchHelper(
                d,
                logger,
                "follow",
                follow,
                unfollow_start,
                passive=passive,
            )
        ct = 0
        unfollow_count = update_count("unfollowed", view_only=True)
        while unfollow_count > UNFOLLOW_DAILY_LIMIT:
            print(f"unfollowed: {unfollow_count}, sleeping...")
            switch_h.sleep_countdown(1300, 1300)
            tracking_data(d, logger)
            unfollow_count = update_count("unfollowed", view_only=True)

        unfollow_start(d, logger)

        while 1:
            try:
                if unfollow_count > UNFOLLOW_DAILY_LIMIT:
                    print(f"unfollowed: {unfollow_count}, sleeping...")
                    switch_h.sleep_countdown(1300, 1300)
                    tracking_data(d, logger)
                    unfollow_count = update_count("unfollowed", view_only=True)
                    if unfollow_count == 0:
                        unfollow_start(d, logger)
                    continue

                # loop through users
                for x in d(resourceId="com.zhiliaoapp.musically:id/a3f"):
                    if x.info["text"] != "Following":
                        continue
                    ct += 1
                    if ct % 5 == 0:
                        logger.info(f"Total unfollowed: {ct}")

                    unfollow_count = update_count("unfollowed")
                    if unfollow_count is None:
                        tracking_data(d, logger)
                        unfollow_count = update_count("unfollowed", view_only=True)
                        raise Exception("New day, updating df...")

                    x.click()
                    switch_h.sleep_countdown(5, 80)

                    rand_num = random.randint(0, 80)
                    # random sleep
                    if 3 < rand_num < 9:
                        logger.info(f"Random number: {rand_num}, sleeping")
                        switch_h.sleep_countdown(50, 2000)

                    # random restart
                    elif rand_num < 3:
                        logger.info(f"Random number: {rand_num}, restarting")
                        unfollow_start(d, logger)

                # scroll the page after explored all users
                d.swipe(400, 400, 400, 100, 0.03)
                switch_h.sleep_countdown(5, 20)

            except Exception as e:
                """
                catch uiautomator2.exceptions.UiObjectNotFoundError
                """
                logger.error(f"Unfollow Error: {e}\nRestarting TikTok!")
                d.screenshot(
                    f"screenshots\\{'Unfollow Error'} {datetime.datetime.now().strftime('%m.%d %H-%M-%S')}.jpg"
                )
                unfollow_start(d, logger)

    except KeyboardInterrupt:
        pass

    except Exception as e:
        logger.error(f"Unfollow Error: {e}\nRestarting Android Emulator!")
        d.screenshot(
            f"screenshots\\{'Unfollow Error'} {datetime.datetime.now().strftime('%m.%d %H-%M-%S')}.jpg"
        )
        restart_android_emulator()
        unfollow(d, logger, passive)

    logger.info(f"Unfollowed: {ct}, exited")


if __name__ == "__main__":
    from follow_bot import follow

    os.system("adb devices")
    d = u2.connect()
    logger = create_logger("unfollow")
    df = tracking_data(d, logger)

    unfollow(d, logger)
