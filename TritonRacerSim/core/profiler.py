'''Timing all the parts'''
import time

class Profiler: 
    def __init__(self):
        self.profiles = {}
        pass

    def watch(self, component):
        self.begin_time = time.time()

    def stop_watch(self, component):
        duration = (time.time() - self.begin_time) * 1000
        self.profiles[component.getName()] = duration

    def dump(self):
        for component_name, duration in self.profiles.items():
            print (f'{component_name}: {duration} ms')