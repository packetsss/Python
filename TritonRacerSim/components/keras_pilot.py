import time
import os
import queue
from os import path
import numpy as np
from PIL import Image
import tensorflow as tf

from tensorflow.python.keras.models import load_model

from TritonRacerSim.components.component import Component
from TritonRacerSim.components.controller import DriveMode
from TritonRacerSim.utils.types import ModelType
from TritonRacerSim.utils.mapping import calcBreak, calcThrottle


class KerasPilot(Component):
    def __init__(self, cfg, model_path, model_type):
        inputs = ['cam/img', 'gym/speed', 'loc/segment', 'gym/cte', 'usr/mode']
        outputs = ['ai/steering', 'ai/throttle', 'ai/breaking']
        self.model_type = model_type
        if model_type == ModelType.CNN_2D:
            pass

        Component.__init__(self, inputs=inputs, outputs=outputs, threaded=False)
        self.model = load_model(model_path, compile=True)
        self.model.summary()
        tf.keras.backend.set_learning_phase(0)
        self.on = True

        self.speed_control_threshold = cfg['spd_ctl_threshold']
        self.speed_control_reverse = cfg['spd_ctl_reverse']
        self.speed_control_break = cfg['spd_ctl_break']
        self.speed_control_reverse_multiplier = cfg['spd_ctl_reverse_multiplier']
        self.speed_control_break_multiplier = cfg['spd_ctl_break_multiplier']

        self.smooth_steering = cfg['smooth_steering_enabled']
        self.smooth_steering_threshold = cfg['smooth_steering_threshold']

        if self.smooth_steering:
            print('[WARNING] Smooth-Steering Enabled')

        self.cfg = cfg
    
    def step(self, *args):
        if args[0] is None:
            return 0.0, 0.0, 0.0
        if  args[-1] == DriveMode.AI_STEERING or args[-1] == DriveMode.AI:
            img_arr = np.asarray(args[0],dtype=np.float32)
            img_arr /= 255
            #img = Image.fromarray(img_arr)
            #plt.imshow(img)
            #plt.show()
            #plt.clf()
            img_arr = img_arr.reshape((1,) + img_arr.shape)
            
            if self.model_type == ModelType.CNN_2D:
                # start_time = time.time()
                steering_and_throttle = self.model(img_arr)
                # print(f'Prediction time: {time.time() - start_time}')
                steering, throttle = self.__cap(steering_and_throttle.numpy()[0])

                steering = self.__smooth_steering(steering)

                return steering, throttle, 0.0

            elif self.model_type == ModelType.CNN_2D_SPD_FTR:
                spd = np.asarray((args[1] / 20,), dtype=np.float32)
                spd = spd.reshape((1,) + spd.shape) 
                # print (img_arr.shape)
                steering_and_throttle = self.model((img_arr, spd))
                steering, throttle = self.__cap(steering_and_throttle.numpy()[0])

                steering = self.__smooth_steering(steering)

                return steering, throttle, 0.0

            elif self.model_type == ModelType.CNN_2D_SPD_CTL:
                # print (img_arr.shape)
                real_spd = args[1]
                steering_and_speed = self.model(img_arr)
                steering = self.__cap(steering_and_speed.numpy()[0][0])
                predicted_speed = steering_and_speed.numpy()[0][1] * 20
                breaking = 0.0

                throttle = calcThrottle(real_spd, predicted_speed * self.speed_control_threshold, self.speed_control_reverse_multiplier)

                if self.speed_control_break:
                    throttle = 1.0 if predicted_speed - real_spd > 0.0 else 0.0
                    breaking = calcBreak(real_spd, predicted_speed * self.speed_control_threshold, self.speed_control_break_multiplier)
                # print (f'Spd: {real_spd}, Pred: {predicted_speed} \r', end='')
                print (f'Thr: {throttle}, Brk: {breaking} \r', end='')
                steering = self.__smooth_steering(steering)
                
                return steering, throttle, breaking

            elif self.model_type == ModelType.CNN_2D_FULL_HOUSE:
                # print (args[1], args[2], args[3])
                real_spd = args[1]
                spd = np.asarray(real_spd/20, dtype=np.float32)
                spd = spd.reshape((1,) + spd.shape)
                features = np.asarray((args[2],), dtype=np.float32)
                features = features.reshape((1,) + features.shape)
                steering_and_speed = self.model((img_arr, spd, features))
                steering = self.__cap(steering_and_speed.numpy()[0][0])
                predicted_speed = steering_and_speed.numpy()[0][1] * 20
                breaking = 0.0
                # print (f'Spd: {real_spd}, Pred: {predicted_speed} \r', end='')
                throttle = calcThrottle(real_spd, predicted_speed * self.speed_control_threshold, self.speed_control_reverse_multiplier)

                if self.speed_control_break:
                    throttle = 1.0 if predicted_speed - real_spd > 0.0 else 0.0
                    breaking = calcBreak(real_spd, predicted_speed * self.speed_control_threshold, self.speed_control_break_multiplier)
               
                print (f'Thr: {throttle}, Brk: {breaking} \r', end='')
                steering = self.__smooth_steering(steering)
                
                return steering, throttle, breaking
                '''
                if (predicted_speed * self.speed_control_threshold > real_spd): # Accelerate to match the predicted speed
                    throttle = 1.0
                else:
                    throttle = 0.0 # Decelerate to match the predicted speed
                    breaking = 0.0

                steering = self.__smooth_steering(steering)

                return steering, throttle, breaking
                '''
        return 0.0, 0.0, 0.0

    def onStart(self):
        if self.cfg['preprocessing_enabled']:
            print('[WARNING] Image preprocessing is enabled. Autopilot is fed with FILTERED image.')

    def onShutdown(self):
        self.on = False
            
    def getName(self):
        return 'Keras Pilot'

    def __cap(self, val):
        if val < -1.0: val = -1.0
        elif val > 1.0: val = 1.0
        return val

    def __smooth_steering(self, val):
        if self.smooth_steering:
            if val > self.smooth_steering_threshold:
                val = 1.0
            elif val < self.smooth_steering_threshold * -1:
                val = -1.0
        return val


class PilotTester:
    def __init__(self):
        model_path = path.abspath('./try.h5')

        self.pilot = KerasPilot(model_path, ModelType.CNN_2D)
        pass

    def test(self):
        for i in range(6, 20):
            img_path = path.abspath('./data/valid/records_4/img_{}.jpg'.format(i))
            img_arr = np.asarray(Image.open(img_path))
            self.pilot.step(img_arr, DriveMode.AI)
        self.pilot.onShutdown()

#test = PilotTester()
#test.test()