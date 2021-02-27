from TritonRacerSim.components.component import Component

class PCA9685 (Component):
    def __init__(self, cfg):
        super().__init__(inputs=['mux/steering', 'mux/throttle'], outputs=[], threaded=False)
        self.left_pulse = cfg['calibrate_max_left_pwm']
        self.right_pulse = cfg['calibrate_max_right_pwm']
        self.neutral_steering_pulse = cfg['calibrate_neutral_steering_pwm']
        self.max_pulse = cfg['calibrate_max_forward_pwm']
        self.min_pulse = cfg['calibrate_max_reverse_pwm']
        self.zero_pulse = cfg['calibrate_zero_throttle_pwm']

    def onStart(self):
        """Called right before the main loop begins"""
        pass

    def step(self, *args):
        """The component's behavior in the main loop"""
        pass

    def onShutdown(self):
        """Shutdown"""
        pass

    def getName(self):
        return 'PCA9685'