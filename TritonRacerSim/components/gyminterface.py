from TritonRacerSim.components.component import Component
from PIL import Image
import os
import random
import json
import time
from io import BytesIO
import base64
import numpy as np
from gym_donkeycar.core.sim_client import SDClient

'''Code Reference:
https://github.com/tawnkramer/sdsandbox/blob/master/src/test_client.py
'''

DEFAULT_GYM_CONFIG = {
    'racer_name': 'Triton Racer',
    'bio' : 'Triton-AI',
    'country' : 'US',
    "guid": "comeondowntosouthparkandmeetsomefriendsofmine",

    'body_style' : 'car01', 
    'body_rgb': (24, 43, 73),
    'car_name' : 'Trident',
    'font_size' : 50,

    "fov" : 80, 
    "fish_eye_x" : 0.0, 
    "fish_eye_y" : 0.0, 
    "img_w" : 160, 
    "img_h" : 120, 
    "img_d" : 3, 
    "img_enc" : 'JPG', 
    "offset_x" : 0.0, 
    "offset_y" : 3, 
    "offset_z" : 1.0, 
    "rot_x" : 0.0,
    # "rot_y": 180,

    'scene_name': 'generated_track',
    'sim_host': '127.0.0.1',
    # 'sim_host':'donkey-sim.roboticist.dev',
    'sim_port': 9091,
    'sim_latency': 0
}

class GymInterface(Component, SDClient):
    '''Talking to the donkey gym'''
    def __init__(self, poll_socket_sleep_time=0.01, gym_config = DEFAULT_GYM_CONFIG):
        self.gym_config = DEFAULT_GYM_CONFIG
        self.gym_config.update(gym_config)
        Component.__init__(self, inputs=['mux/steering', 'mux/throttle', 'mux/breaking', 'usr/reset'], outputs=['cam/img', 'gym/x', 'gym/y', 'gym/z', 'gym/speed', 'gym/cte'], threaded=False)
        SDClient.__init__(self, self.gym_config['sim_host'], self.gym_config['sim_port'], poll_socket_sleep_time=poll_socket_sleep_time)
        self.load_scene(self.gym_config['scene_name'])
        self.send_config()
        self.last_image = None
        self.car_loaded = False
        self.latency = self.gym_config['sim_latency']

        self.pos_x = 0.0
        self.pos_y = 0.0
        self.pos_z = 0.0
        self.speed = 0.0
        self.cte = 0.0
    
    def step(self, *args):
        steering = args[0]
        throttle = args[1]
        breaking = args[2]
        if breaking is None: breaking = 0.0
        reset = args[3]
        self.send_controls(steering, throttle, breaking)
        if reset:
            self.reset_car()

        return self.last_image, self.pos_x, self.pos_y, self.pos_z, self.speed, self.cte

    def onStart(self):
        print(f'CAUTION: Confirm your artificial latency setting: {self.latency}ms.')

    def onShutdown(self):
        self.stop()
        
    def getName(self):
        return 'Gym Interface'

    def on_msg_recv(self, json_packet):
        if json_packet['msg_type'] == "need_car_config":
            self.send_config()

        elif json_packet['msg_type'] == "car_loaded":
            print('Car loaded.')
            self.car_loaded = True
        
        elif json_packet['msg_type'] == "telemetry":
            time.sleep(self.gym_config['sim_latency'] / 1000.0) # 1000 for ms -> s
            imgString = json_packet["image"]
            image = Image.open(BytesIO(base64.b64decode(imgString)))
            self.last_image = np.asarray(image, dtype=np.uint8)
            self.pos_x = float(json_packet['pos_x'])
            self.pos_y = float(json_packet['pos_y'])
            self.pos_z = float(json_packet['pos_z'])
            self.speed = float(json_packet['speed'])
            self.cte = float(json_packet['cte'])

    def send_config(self):
        '''
        send three config messages to setup car, racer, and camera
        '''
        print('Sending configs...')
        print('Sending racer info')
        # Racer info
        msg = {'msg_type': 'racer_info',
            'racer_name': self.gym_config['racer_name'],
            'car_name' : self.gym_config['car_name'],
            'bio' : self.gym_config['bio'],
            'country' : self.gym_config['country'],
            'guid': self.gym_config['guid'] }
        self.send_now(json.dumps(msg))

        time.sleep(1.0)

        print('Sending car config')
        # Car config
        msg = { "msg_type" : "car_config", 
        "body_style" : self.gym_config['body_style'], 
        "body_r" : self.gym_config['body_rgb'][0].__str__(), 
        "body_g" : self.gym_config['body_rgb'][1].__str__(), 
        "body_b" : self.gym_config['body_rgb'][2].__str__(), 
        "car_name" : self.gym_config['car_name'], 
        "font_size" : self.gym_config['font_size'].__str__() }
        self.send_now(json.dumps(msg))

        #this sleep gives the car time to spawn. Once it's spawned, it's ready for the camera config.
        time.sleep(1.0)
        '''
        # Camera config     
        msg = { "msg_type" : "cam_config", 
        "fov" : self.gym_config['fov'].__str__(), 
        "fish_eye_x" : self.gym_config['fish_eye_x'].__str__(), 
        "fish_eye_y" : self.gym_config['fish_eye_y'].__str__(), 
        "img_w" : self.gym_config['img_w'].__str__(), 
        "img_h" : self.gym_config['img_h'].__str__(), 
        "img_d" : self.gym_config['img_d'].__str__(), 
        "img_enc" : self.gym_config['img_enc'], 
        "offset_x" : self.gym_config['offset_x'].__str__(), 
        "offset_y" : self.gym_config['offset_y'].__str__(), 
        "offset_z" : self.gym_config['offset_z'].__str__(), 
        "rot_x" : self.gym_config['rot_x'].__str__() 
        }
        self.send_now(json.dumps(msg))
        '''
        print (f"Gym Interface: Camera resolution ({self.gym_config['img_w']}, {self.gym_config['img_h']}).")
        

    def send_controls(self, steering, throttle, breaking):
        msg = { "msg_type" : "control",
                "steering" : steering.__str__(),
                "throttle" : throttle.__str__(),
                "brake" : breaking.__str__() }
        self.send(json.dumps(msg))

        #this sleep lets the SDClient thread poll our message and send it out.
        # time.sleep(self.poll_socket_sleep_sec)

    def load_scene(self, scene):
        print(f'Loading scene: {scene}')
        msg = {"msg_type" : "load_scene", "scene_name" : scene}
        self.send_now(json.dumps(msg))

    def reset_car(self):
        print('Resetting car...')
        msg = {'msg_type': 'reset_car'}
        self.send(json.dumps(msg))