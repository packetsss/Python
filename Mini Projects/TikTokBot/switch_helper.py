import ctypes
import random
import threading
from time import sleep


class ExcThread(threading.Thread):
    def __init__(self, func, logger):
        threading.Thread.__init__(self)
        self.func = func
        self.logger = logger

    def run(self):
        try:
            self.func()
        except KeyboardInterrupt:
            return

    def get_id(self):
        if hasattr(self, "_thread_id"):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            thread_id, ctypes.py_object(KeyboardInterrupt)
        )
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            self.logger.error("Exception raise failure")


class SwitchHelper:
    def __init__(
        self,
        d,
        logger,
        filename=None,
        func=None,
        own_func=None,
        passive=False,
    ):
        self.d = d
        self.logger = logger
        self.passive = passive
        if not self.passive:
            self.func = func
            self.own_func = own_func
            self.filename = filename

    def run_another_program(self):
        self.func(self.d, self.logger, True)

    def sleep_countdown(self, min_, max_, threshold=3000):
        sleep_time = random.randint(min_, max_)
        if self.passive:
            sleep_time = int(min(sleep_time, threshold / 3))

        if sleep_time >= threshold and not self.passive:
            self.logger.info(f"Sleep time: {sleep_time}s, executing {self.filename}")
            t = ExcThread(self.run_another_program, self.logger)
            t.start()

            # sleep
            for secs in range(sleep_time, 0, -10):
                sleep(10)
                print(" " * 28, f"{self.filename} remaining:", secs - 1, "\r", end="")
            print(" " * 50, "\r", end="")

            t.raise_exception()
            t.join()
            self.logger.info("Sleep completed, restoring original session")

            self.own_func(self.d, self.logger)
        else:
            for secs in range(sleep_time, 0, -1):
                sleep(1)
                print("Sleep remaining:", secs - 1, "\r", end="")
        print(" " * 25, "\r", end="")
