from enum import Enum
import time
import sched
import re

def __poll(self):
        """Get input values from Teensy in manual mode"""
        while not self.ser.in_waiting:
            pass

        mcu_message = self.ser.readline().decode().lower()  # The message coming in
        sbc_message = 'poll'  # The message to be sent back. a single 'poll' means polling every information
        number_in_message = re.findall(r'\d+\.*\d*', mcu_message)  # Find number in message

        self.watchdog_subthread.reset_countdown()  # Reset watchdog as soon as data is received
        if 'speed' in mcu_message:
            self.speed = number_in_message[0]
            sbc_message += 'Speed'
        elif 'throttle' in mcu_message:
            self.throttle = number_in_message[0]
            sbc_message += 'Throttle'
        elif 'steering' in mcu_message:
            self.steering = number_in_message[0]
            sbc_message += 'Steering'

        self.send(sbc_message + '\n')

class Watchdog:
    """Trigger the callback function if timer reaches threshold (ms), unless reset"""

    def __init__(self, threshold, callback):
        self.threshold = threshold / 1000.0
        self.callback = callback
        self.reset = True
        self.running = True

    def start_watchdog(self, delay=500):
        """Start the watchdog countdown after the delay (ms)"""
        delay_second = delay / 1000.0
        print(f'Watchdog will be engaged in {delay_second} seconds.')
        from threading import Thread
        t = Thread(target=self.__watching, args=(delay,), daemon=False)
        t.start()

    def __watching(self, delay):
        delay_second = delay / 1000.0
        time.sleep(delay_second)

        while self.running:
            if (self.reset):
                self.reset = False
            else:
                self.callback()
            time.sleep(self.threshold)

    def reset_countdown(self):
        """Reset the watchdog countdown"""
        self.reset = True

    def shutdown(self):
        """End the watchdog"""
        self.running = False

def q():
    print("AJ")

uuu = Watchdog(1000, q)

# while 1 == 1:
uuu.start_watchdog(delay=20)
a = input(" ")
