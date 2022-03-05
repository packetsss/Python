import random
import logging
from time import sleep
import uiautomator2 as u2

from utils import *
from config import *
from switch_helper import SwitchHelper


def follow_start(d: u2.Device, logger: logging.Logger) -> None:
    from utils import start

    while not start(d):
        logger.warning("TikTok started failed, retrying...")
        

    d.click(630, 91)
    sleep(0.5)

    # don't sync facebook popup
    if d(text="Don't allow").exists:
        d(text="Don't allow").click()

    sleep(0.5)
    rand_acc = random.choice(HIT_ACCOUNTS)
    d.set_clipboard(rand_acc, 'account_name')
    print(d.clipboard)
    d.long_click(191, 91, 0.8)
    sleep(0.5)
    d.click(147, 185)
    sleep(0.5)
    d.click(625, 85)
    # d.set_fastinput_ime(True)
    # d.send_keys(rand_acc)
    # d.set_fastinput_ime(False)
    # sleep(0.5)
    # d.send_action("search")
    sleep(2)

    # for x in d(className="android.widget.FrameLayout"):
    #     if x.info["bounds"]["bottom"] == 458:
    #         x.click()
    #         break
    d(resourceId="com.zhiliaoapp.musically:id/fqd").click()
    sleep(3)
    d(text="Followers").click()
    sleep(0.5)


def follow(d: u2.Device, logger: logging.Logger, passive: bool = False) -> None:
    try:
        ct = 0
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
                "unfollow",
                unfollow,
                follow_start,
                passive=passive,
            )
        follow_count = update_count("followed", view_only=True)
        while follow_count > FOLLOW_DAILY_LIMIT:
            print(f"followed: {follow_count}, sleeping...")
            switch_h.sleep_countdown(1300, 1300)
            tracking_data(d, logger)
            follow_count = update_count("followed", view_only=True)

        follow_start(d, logger)

        while 1:
            try:
                if follow_count > FOLLOW_DAILY_LIMIT:
                    print(f"followed: {follow_count}, sleeping...")
                    switch_h.sleep_countdown(1300, 1300)
                    tracking_data(d, logger)
                    follow_count = update_count("followed", view_only=True)
                    if follow_count == 0:
                        follow_start(d, logger)
                    continue

                for x in d(resourceId="com.zhiliaoapp.musically:id/ffq"):
                    switch_h.sleep_countdown(1, 20)
                    # make sure only check people I haven't followed
                    if (
                        x.child(resourceId="com.zhiliaoapp.musically:id/a1d").info[
                            "text"
                        ]
                        != "Follow"
                    ):
                        continue

                    x.sibling(
                        className="android.widget.FrameLayout"
                    ).click()  # enter personal page
                    switch_h.sleep_countdown(3, 4)

                    # check counts
                    following = text_to_num(
                        d(resourceId="com.zhiliaoapp.musically:id/bas").info["text"]
                    )
                    followers = text_to_num(
                        d(resourceId="com.zhiliaoapp.musically:id/bah").info["text"]
                    )
                    like = text_to_num(
                        d(resourceId="com.zhiliaoapp.musically:id/ao4").info["text"]
                    )
                    switch_h.sleep_countdown(1, 3)
                    if (
                        FOLLOWING_LIMIT[1] > following > FOLLOWING_LIMIT[0]
                        and FOLLOWERS_LIMIT[1] > followers > FOLLOWERS_LIMIT[0]
                        and LIKE_LIMIT[1] > like > LIKE_LIMIT[0]
                    ):  # follow if condition met
                        d(resourceId="com.zhiliaoapp.musically:id/de0").click()

                        if d(resourceId="com.zhiliaoapp.musically:id/cy1").exists:
                            sleep(0.5)
                            logging.info("Something wrong with this user, moving on...")
                            d(resourceId="com.zhiliaoapp.musically:id/cy1").click()

                        # successfully followed
                        follow_count = update_count("followed")
                        if follow_count is None:
                            tracking_data(d, logger)
                            follow_count = update_count("followed", view_only=True)
                            raise Exception("New day, updating df...")

                        ct += 1
                        if ct % 5 == 0:
                            logger.info(f"Total followed: {ct}")
                        switch_h.sleep_countdown(3, 80)

                    d(resourceId="com.zhiliaoapp.musically:id/nav_start").click()

                    rand_num = random.randint(0, 90)
                    # random sleep
                    if 3 < rand_num < 7:
                        logger.info(f"Random number: {rand_num}, sleeping")
                        switch_h.sleep_countdown(20, 900)

                    # random restart
                    if rand_num < 3:
                        logger.info(f"Random number: {rand_num}, restarting")
                        follow_start(d, logger)

                # scroll the page after followed all
                d.swipe(400, 400, 400, 100, 0.03)
                switch_h.sleep_countdown(5, 20)

            except Exception as e:
                """
                catch uiautomator2.exceptions.UiObjectNotFoundError
                """
                logger.error(f"Follow Error: {e}\nRestarting TikTok!")
                d.screenshot(
                    f"screenshots\\{'Follow Error'} {datetime.datetime.now().strftime('%m.%d %H-%M-%S')}.jpg"
                )
                follow_start(d, logger)

    except KeyboardInterrupt:
        pass

    except Exception as e:
        logger.error(f"Follow Error: {e}\nRestarting Android Emulator!")
        d.screenshot(
            f"screenshots\\{'Follow Error'} {datetime.datetime.now().strftime('%m.%d %H-%M-%S')}.jpg"
        )
        restart_android_emulator()
        follow(d, logger, passive)

    logger.info(f"Followed: {ct}, exited")


if __name__ == "__main__":
    from unfollow_bot import unfollow

    os.system("adb devices")
    d = u2.connect()
    logger = create_logger("follow")
    df = tracking_data(d, logger)

    follow(d, logger)
