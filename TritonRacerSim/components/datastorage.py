from TritonRacerSim.components.component import Component
from pathlib import Path
from os import path
import os
from PIL import Image
import json
from threading import Thread
import sys
import time
import queue

class DataStorage(Component):
    def __init__(self, to_store=['cam/img', 'mux/throttle', 'mux/steering', 'mux/break', 'gym/speed', 'loc/segment', 'gym/x', 'gym/y', 'gym/z', 'gym/cte'], storage_path = None):
        super().__init__(inputs=to_store, threaded=False)
        self.step_inputs += ['usr/del_record', 'usr/toggle_record']
        self.on = True
        self.storage_path = self.__getStoragePath() if storage_path is None else storage_path
        os.mkdir(self.storage_path)
        self.count = 0
        self.recording = False
        self.records_temp = queue.Queue() #temporary storage of records in memory, awaiting file io
        self.file_thread = Thread(target=self.file_io_thread, daemon=True)
        self.file_thread.start()

    def step(self, *args):
        #delete records
        if args[-2]:
            self.__delRecords(100)
        # store records
        elif args[-1]:          
            record = {self.step_inputs[i]: args[i] for i in range(len(self.step_inputs))}
            self.records_temp.put(record)
            self.count += 1

    def onStart(self):
        self.on = True
        # print(f'Data Storage: Variables to Store: {self.step_inputs}')

        status = 'ON' if self.recording else 'OFF'
        print(f'Data Storage: Recording is {status}')

    def onShutdown(self):
        """Shutdown"""
        self.on = False
        if not len(os.listdir(self.storage_path)): # Delete the data folder if there is no data collected
            os.rmdir(self.storage_path)
            print(f'{self.storage_path} has been DELETED since no data was recorded in this session.')


    def getName(self):
        return 'Data Storage'
        
    def __getStoragePath(self):
        car_path = sys.path[0]
        data_dir = path.join(car_path, 'data/')

        if not path.exists(data_dir):
            os.mkdir(data_dir)

        i = 1
        while path.exists(path.join(data_dir, self.__get_record_folder_name(i))):
            i += 1
        
        dir_path = path.join(data_dir, self.__get_record_folder_name(i))
        return dir_path

    def __store(self, count, record={}):
        self.__storeImg(count, record)
        record_path = path.join(self.storage_path, f'record_{count}.json')
        with open(record_path, 'w') as recordFile:
            json.dump(record, recordFile)


    def __storeImg(self, count, record={}):
        img_string = 'cam/img' if 'cam/img' in record else 'cam/processed_img'
        if  record[img_string] is not None:
            img_path = path.join(self.storage_path, f'img_{count}.jpg')
            Image.fromarray(record[img_string]).save(img_path)
            record[img_string] = f'img_{count}.jpg'

    def __delRecords(self, num):
        # original_count = self.count
        self.count -= num
        
        if self.count < 0:
            self.count = 0
        '''
        for i in range(self.count, original_count):
            img_path = path.join(self.storage_path, f'img_{i}.jpg')
            record_path = path.join(self.storage_path, f'record_{i}.json')
            os.remove(img_path)
            os.remove(record_path)
        '''

    def __get_record_folder_name(self, idx):
        return f'records_{idx}/'

    def file_io_thread(self):
        # a seperate thread for file io
        count = self.count
        sleep_s = 0.005

        while self.on:
            while count == self.count:
                time.sleep(sleep_s)

            if (count > self.count): #delete record
                count = self.count
            else:# save record
                if self.records_temp:
                    self.__store(count, self.records_temp.get())
                    count += 1

            if count % 100 == 0:
                print (f'Collected {count} records')



        

