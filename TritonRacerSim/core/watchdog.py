import time
import sched

class Watchdog:
    """Trigger the callback function if timer reaches threshold (ms), unless reset"""

    def __init__(self, threshold=100, callback=None):
        self.threshold = threshold / 1000.0
        self.timeElapsed = None
        self.callback = callback
        self.sche = sched.scheduler(time.time, time.sleep)

    def start_watchdog(self, delay=500):
        """Start the watchdog countdown after the delay (ms)"""
        delay_second = delay / 1000.0
        self.sche.enter(delay_second, 1, self.__watching)

    def __watching(self):
        self.sche.enter(self.threshold, 1, self.callback)

    def reset_countdown(self):
        """Reset the watchdog countdown"""
        list(map(self.sche.cancel, self.sche.queue))
        self.__watching()

    def shutdown(self):
        """End the watchdog"""
        list(map(self.sche.cancel, self.sche.queue))