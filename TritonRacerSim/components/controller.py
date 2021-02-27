from typing import List
import pygame
import time
import os
import json

from pygame import joystick
from TritonRacerSim.components.component import Component
from enum import Enum


class DriveMode(Enum):
    HUMAN = 'human'
    AI_STEERING = 'ai_steering'
    AI = 'ai'


class JoystickType(Enum):
    PS4 = 'ps4'
    PS3 = 'ps3'
    XBOX = 'xbox'
    G28 = 'g28'
    SWITCH = 'switch'
    STEAM = 'steam'
    F710 = 'f710'
    CUSTOM = 'custom'


class Controller(Component):
    '''Generic base class for controllers'''

    def __init__(self, cfg):
        Component.__init__(self, threaded=True,
                           outputs=['usr/steering', 'usr/throttle', 'usr/breaking', 'usr/mode', 'usr/del_record',
                                    'usr/toggle_record', 'usr/reset'])
        self.mode = DriveMode(cfg['default_drive_mode'])
        self.del_record = False
        self.toggle_record = False
        self.reset = False
        self.steering = 0.0
        self.throttle = 0.0
        self.breaking = 0.0
        self.cfg = cfg

    def getName(self):
        return 'Generic Controller'


PS4_CONFIG = {'steering_axis': 0, 'throttle_axis': 4, 'break_axis': 5, 'toggle_mode_but': 8, 'del_record_but': 2,
              'toggle_record_but': 1, 'reset_but': 3, 'has_break': True}
G28_CONFIG = {'steering_axis': 0, 'throttle_axis': 2, 'break_axis': 3, 'toggle_mode_but': 8, 'del_record_but': 2,
              'toggle_record_but': 1, 'reset_but': 3, 'has_break': True}
XBOX_CONFIG = {'steering_axis': 0, 'throttle_axis': 4, 'break_axis': 5, 'toggle_mode_but': 6, 'del_record_but': 3,
               'toggle_record_but': 1, 'reset_but': 2, 'has_break': True}
PS4_BLUETOOTH_CONFIG = {'steering_axis': 0, 'throttle_axis': 5, 'break_axis': 4, 'toggle_mode_but': 8,
                        'del_record_but': 2, 'toggle_record_but': 1, 'reset_but': 3, 'has_break': True}
STEAM_CONFIG = {'steering_axis': 0, 'throttle_axis': 1, 'break_axis': 2, 'toggle_mode_but': 6, 'del_record_but': 2,
                'toggle_record_but': 1, 'reset_but': 3, 'has_break': True}
SWITCH_CONFIG = {'steering_axis': 0, 'throttle_axis': 3, 'break_axis': 2, 'toggle_mode_but': 13, 'del_record_but': 0,
                 'toggle_record_but': 1, 'reset_but': 3, 'has_break': False}
F710_CONFIG = {'steering_axis': 0, 'throttle_axis': 4, 'break_axis': 5, 'toggle_mode_but': 6, 'del_record_but': 3,
               'toggle_record_but': 1, 'reset_but': 2, 'has_break': True}


class PygameJoystick(Controller):
    def __init__(self, cfg):
        Controller.__init__(self, cfg)
        joystick_type = cfg['type']
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()
        pygame.joystick.init()
        has_joystick = pygame.joystick.get_count()
        if has_joystick == 0:
            raise Exception('No joystick detected')
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.on = True
        print(f'Joystick name: {self.joystick.get_name()}')

        if JoystickType(joystick_type) == JoystickType.PS4:
            if not cfg['use_bluetooth']:
                self.joystick_map = PS4_CONFIG
            else:
                self.joystick_map = PS4_BLUETOOTH_CONFIG
        elif JoystickType(joystick_type) == JoystickType.G28:
            self.joystick_map = G28_CONFIG
        elif JoystickType(joystick_type) == JoystickType.XBOX:
            self.joystick_map = XBOX_CONFIG
        elif JoystickType(joystick_type) == JoystickType.SWITCH:
            self.joystick_map = SWITCH_CONFIG
        elif JoystickType(joystick_type) == JoystickType.F710:
            self.joystick_map = F710_CONFIG
        elif JoystickType(joystick_type) == JoystickType.CUSTOM:
            self.joystick_map = self.__load_joystick_config(cfg['custom_mapping_file'])
        else:
            raise Exception('Unsupported joystick')

    def step(self, *args):
        to_return = (
        self.steering, self.throttle, self.breaking, self.mode, self.del_record, self.toggle_record, self.reset)
        self.del_record = False
        self.reset = False
        return to_return

    def thread_step(self):
        # function map
        poll_interval = 10  # ms
        poll_interval /= 1000.0

        # Function map: trigger the corresponding function according to which button is pressed.
        switcher = {self.joystick_map['del_record_but']: self.__delRecord,
                    self.joystick_map['toggle_record_but']: self.__toggleRecord,
                    self.joystick_map['toggle_mode_but']: self.__toggleMode,
                    self.joystick_map['reset_but']: self.__reset
                    }
        while self.on:
            self.steering = self.map_steering(self.joystick.get_axis(self.joystick_map['steering_axis']))
            self.throttle = self.map_throttle(self.joystick.get_axis(self.joystick_map['throttle_axis']))

            self.steering = self.limit_steering(self.steering)
            self.throttle = self.limit_throttle(self.throttle)

            if self.joystick_map['has_break']:
                self.breaking = self.map_break(self.joystick.get_axis(self.joystick_map['break_axis']))

            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button in switcher:
                        switcher[event.button]()
            time.sleep(poll_interval)

    def onShutdown(self):
        self.on = False
        pygame.quit()

    def getName(self):
        return 'Generic Pygame Joystick'

    def __toggleMode(self):
        if self.mode == DriveMode.HUMAN:
            self.mode = DriveMode.AI_STEERING
        elif self.mode == DriveMode.AI_STEERING:
            self.mode = DriveMode.AI
        elif self.mode == DriveMode.AI:
            self.mode = DriveMode.HUMAN
        print(f'Mode: {self.mode}')
        return self.mode

    def __delRecord(self):
        self.del_record = True
        print('Deleting records')

    def __toggleRecord(self):
        if self.toggle_record:
            self.toggle_record = False
            print('Recording paused.')
        else:
            self.toggle_record = True
            print('Recording started.')

    def __reset(self):
        self.reset = True
        print('Car reset.')

    @staticmethod
    def __limit_val(val, limit):
        return val * limit

    def __load_joystick_config(file):
        with open(file, 'r') as input:
            config = json.load(input)
        return config

    def limit_throttle(self, val):
        return self.__limit_val(val, self.cfg['joystick_max_throttle'])

    def limit_steering(self, val):
        return self.__limit_val(val, self.cfg['joystick_max_steering'])

    def map_steering(self, val):
        return val

    def map_throttle(self, val):
        return val

    def map_break(self, val):
        return val


class G28DrivingWheel(PygameJoystick):
    def __init__(self, cfg):
        PygameJoystick.__init__(self, cfg)

    def map_steering(self, val):
        val *= 5
        if val > 1:
            val = 1
        elif val < -1:
            val = -1
        return val

    def map_throttle(self, val):
        val = (val - 1) / 2 * -1
        return val

    def map_break(self, val):
        val = 1 - ((val + 1) / 2)
        if val < 0.01:
            val = 0.0
        return val

    def getName(self):
        return 'G28 Driving Wheel'


class PS4Joystick(PygameJoystick):
    def __init__(self, cfg):
        PygameJoystick.__init__(self, cfg)

    def map_steering(self, val):
        if self.cfg['use_bluetooth']:
            return val * -1
        else:
            return val

    def map_throttle(self, val):
        return val * -1

    def map_break(self, val):
        val = (val + 1) / 2
        if val < 0.2:
            val = 0.0
        return val

    def getName(self):
        return 'PS4 Joystick'


class XBOXJoystick(PygameJoystick):
    def __init__(self, cfg):
        PygameJoystick.__init__(self, cfg)

    def map_steering(self, val):
        return val

    def map_throttle(self, val):
        return val * -1

    def map_break(self, val):
        val = (val + 1) / 2
        if val < 0.2:
            val = 0.0
        return val

    def getName(self):
        return 'XBox Joystick'


class STEAMJoystick(PygameJoystick):
    def __init__(self, cfg):
        PygameJoystick.__init__(self, cfg)

    def map_steering(self, val):
        return val

    def map_throttle(self, val):
        return val * -1

    def map_break(self, val):
        val = (val + 1) / 2
        if val < 0.2:
            val = 0.0
        return val

    def getName(self):
        return 'Steam Joystick'


class SWITCHJoystick(PygameJoystick):
    def __init__(self, cfg):
        PygameJoystick.__init__(self, cfg)

    def map_steering(self, val):
        return val

    def map_throttle(self, val):
        return val * -1

    def map_break(self, val):
        val = (val + 1) / 2
        if val < 0.2:
            val = 0.0
        return val

    def getName(self):
        return 'Switch Joystick'


class DummyJoystick(Controller):
    def step(self, *args):
        return 0.0, 0.0, 0.0, DriveMode.HUMAN, False, False, False

    def getName(self):
        return 'Dummy Joystick'


class F710Joystick(PygameJoystick):
    def __init__(self, cfg):
        PygameJoystick.__init__(self, cfg)

    def map_steering(self, val):
        return val

    def map_throttle(self, val):
        return val * -1

    def map_break(self, val):
        val = (val + 1) / 2
        if val < 0.2:
            val = 0.0
        return val

    def getName(self):
        return 'F710 Joystick'


class CustomJoystickCreator:
    '''Class for creating custom pygame joystick mapping'''

    def __init__(self):
        self.config = {'steering_axis': 0, 'throttle_axis': 4,
                       'break_axis': 5, 'toggle_mode_but': 8,
                       'del_record_but': 2, 'toggle_record_but': 1,
                       'reset_but': 3, 'has_break': True,
                       'reverse_steering': False, 'reverse_throttle': True,
                       'idle_break': -1.0, 'max_break': 1.0
                       }
        self.js = None

    def create(self):
        print("""This custom joystick wizard will assist you in creating your custom joystick
        Please connect your joystick, and hit ENTER to continue...""")
        input()
        self.js = self.select_joystick()
        print("""Hit ENTER to continue...""")
        input()
        str_axis, str_reversed, neutral, max = self.get_max_axis(
            "Pick an axis for steering (cannot be trigger), and pull to FULL LEFT.")
        thr_axis, thr_reversed, neutral, max = self.get_max_axis(
            "Good. Now pick an axis for throttle (cannot be trigger), and pull to FULL FORWARD.")
        print("""Nice. Do you want to map another axis for break?
        You do not need to if you do not have enough axies
        y/[n]: """)
        respond = input
        if respond.lower() == "y":
            has_break = True
            brk_axis, brk_reversed, brk_neutral, brk_max = self.get_max_axis(
                "Nice. Now pick an axis (trigger maybe) for break.")
        else:
            has_break = False
            brk_axis = 0;
            brk_reversed = 0;
            brk_neutral = 0.0;
            brk_max = 0.0
        print("""Good job. Now the buttons.""")
        toggle_mode = self.get_pressed_button("toggling driving mode")
        del_record = self.get_pressed_button("deleting records")
        toggle_record = self.get_pressed_button("toggling recording")
        reset = self.get_pressed_button("resetting the car")

        config = {'steering_axis': str_axis, 'throttle_axis': thr_axis,
                  'break_axis': brk_axis, 'toggle_mode_but': toggle_mode,
                  'del_record_but': del_record, 'toggle_record_but': toggle_record,
                  'reset_but': reset, 'has_break': has_break,
                  'reverse_steering': str_reversed, 'reverse_throttle': thr_reversed,
                  'idle_break': brk_neutral, 'max_break': brk_max
                  }

        file_name = "custom_joystick.json"
        self.write_config(config, file_name)
        print(f"""Custom joystick has been generated and saved in {file_name}.
        Please change joystick_type to \"custom\" to use it.""")

    def select_joystick(self) -> pygame.joystick.Joystick:
        pygame.init()
        pygame.joystick.init()
        js_count = pygame.joystick.get_count()
        print(f"Total number of visible joystick by PyGame: {js_count}")
        js_idx = int(input("Please enter the index of joystick you wish to use (starting from 0): "))
        js = pygame.joystick.Joystick(js_idx)
        js.init()
        print(f"Joystick {js_idx} has been selected.")
        return js

    def dump_joystick(self, js) -> str:
        '''Dump the status of a joystick'''
        js.init()
        dump = ""

        name = js.get_name()
        dump += f"Joystick Name: {name}\n"

        axes = js.get_numaxes()
        for i in range(axes):
            axis_val = js.get_axis(i)
            dump += f"Axis {i}: {axis_val}\n"

        dump += "\n"

        buttons = js.get_numbuttons()
        for i in range(buttons):
            button_val = js.get_button(i)
            dump += f"Button {i}: {button_val}\n"

        dump += "\n"

        hats = js.get_numhats()
        for i in range(hats):
            hat = js.get_hat(i)
            dump += f"Hat {i}: {str(hat)}\n"
        return dump

    def get_max_axis(self, prompt) -> tuple:
        """Return which axis was pulled, whether it was reversed, and the neutral max."""
        print("""First, put your hand off the joystick. 
        Press ENTER to continue...""")
        input()
        neutral_axes = self.get_all_axes()
        while True:
            print(f"""{prompt}
            Hit ENTER while doing so...""")
            input()
            moved_axes = self.get_all_axes()
            from operator import sub
            delta = list(map(sub, neutral_axes, moved_axes))
            abs_delta = list(map(abs, delta))
            moved_axis = abs_delta.index(max(abs_delta))
            if abs_delta[moved_axis] > 0.5:
                reversed = True if moved_axes[moved_axis] < 0 else False
                return moved_axis, reversed, neutral_axes[moved_axes], moved_axes[moved_axis]
            else:
                print("I cannot tell which axis was moved. Try again.")

    def get_all_axes(self) -> list:
        axes = []
        for i in range(self.js.get_numaxes()):
            axes.append(self.js.get_axis(i))
        print(axes)
        return axes

    def get_pressed_button(self, button_prompt: str) -> int:
        buttons = self.js.get_numbuttons()
        while True():
            print(f"Hold the button for {button_prompt}.")
            print("Hit ENTER to continue...")
            input()
            for i in range(buttons):
                button_val = self.js.get_button(i)
                if button_val == 1: return i
            print("No button press was detected. Please hold the button and try again.")

    def write_config(self, config, file_name):
        with open(file_name, 'w') as output:
            json.dump(config, output)


class CustomJoystick(PygameJoystick):
    def __init__(self, cfg):
        PygameJoystick.__init__(self, cfg)
        self.str_rev = self.joystick_map['reverse_steering']
        self.thr_rev = self.joystick_map['reverse_throttle']
        self.brk_idle = self.joystick_map['idle_break']
        self.brk_max = self.joystick_map['max_break']
        self.brk_range = abs(self.brk_max - self.brk_idle)

    def map_steering(self, val):
        return val * -1.0 if self.str_rev else val

    def map_throttle(self, val):
        return val * -1.0 if self.thr_rev else val

    def map_break(self, val):
        if abs(val - self.brk_idle) < 0.15:
            return 0.0
        else:
            return abs(val - self.brk_idle) / self.brk_range

    def getName(self):
        return 'Custom Joystick'