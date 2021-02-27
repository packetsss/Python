from os import path
import json
import time
from PIL import Image

from TritonRacerSim.components.component import Component


class TrackDataProcessor:
    def __init__(self, tub_path, output_path):
        self.tub_path = tub_path
        self.output_path = output_path
        if not path.exists(tub_path):
            raise FileNotFoundError('Cannot find tub {}'.format(tub_path))
        self.line = []

    def process(self):
        i = 1
        while True:
            try:
                data_path = path.join(self.tub_path, 'record_{}.json'.format(i))

                f = open(data_path)
                data = json.load(f)
                f.close()

                point = [data['gym/x'], data['gym/y'], data['gym/z']]
                self.line.append(point)

                i += 1
            except FileNotFoundError:
                break

        print(i, 'points loaded, Saving to ', self.output_path)

        # self.__sort()

        with open(self.output_path, 'w') as output_file:
            json.dump(self.line, output_file)

    def __sort(self):
        '''buggy'''
        original_count = len(self.line)
        newData = []
        last_point = self.line[0]
        selected_i = 0
        
        while len(newData) != original_count:          
            last_distance = 100
            for i, point in enumerate(self.line):
                current_distance = self.__distance(last_point, point)
                if current_distance < last_distance:
                    selected_i = i
                    last_distance = current_distance

            newData.append(self.line[selected_i])
            last_point = newData[-1]
            del self.line[selected_i]
        
        self.line = newData


    def __distance(self, a, b):
        return abs((a[0] - b[0]) + (a[0] - b[0]) + (a[0] - b[0]))



class LocationTracker(Component):
    def __init__(self, track_data_path, min_map = 0, max_map = 10):
        Component.__init__(self, inputs=['gym/x', 'gym/y', 'gym/z'], outputs=['loc/segment'])

        with open(track_data_path, 'r') as input_file:
            self.data = json.load(input_file)
        self.max = max_map
        self.min = min_map

    def localize(self, point):
        idx, duration = self.__find_closest(point)
        return self.__map(idx), duration

    def step(self, *args):
        track_segment, duration = self.localize((args[0], args[1], args[2]))
        # print(f'Segment: {track_segment}, Duration: {duration}\r', end='')
        return track_segment,

    def onShutdown(self):
        pass

    def __find_closest(self, point):
        begin_time = time.time()

        selected_i = 0
        last_distance = 100

        for i, center_point in enumerate(self.data):
            current_distance = self.__distance(point, center_point)
            if current_distance < last_distance:
                    selected_i = i
                    last_distance = current_distance
        duration = time.time() - begin_time
        return selected_i, duration

    def __distance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])    

    def __map(self, idx):
        return idx / float(len(self.data)) * (self.max - self.min) + self.min
            

