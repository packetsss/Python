from TritonRacerSim.components.component import Component


class DriverAssistance (Component):
    '''Automatic steering and throttle limiter'''

    def __init__(self, cfg):
        super().__init__(inputs=['mux/steering', 'mux/throttle', 'mux/break', 'gym/speed'],
                         outputs=['mux/steering', 'mux/throttle', 'mux/break'], threaded=False)
        self.limit_mode = cfg['drive_assist_limit_mode']
        self.k = cfg['drive_assist_limit_k']

    def step(self, *args):
        steering, throttle, breaking, speed = args
        if None not in args:
            if self.limit_mode == 'steering' and speed != 0:
                max_steering = self.k / speed
                if (steering > max_steering):
                    steering = max_steering
                    throttle = -0.1
                elif steering < max_steering * -1:
                    steering = max_steering * -1
                    throttle = -0.1

            elif self.limit_mode == 'speed' and steering != 0:
                max_speed = self.k / steering
                if speed > max_speed:
                    throttle = 0.0 
                    breaking = 0.0

        return steering, throttle, breaking

    def getName(self):
        return 'Driver Assistance'
