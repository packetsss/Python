'''If you have the original images, and you would like to filter the image based on new filter params, use post_processing.'''
import os
import time
import math
from os import mkdir, path
from shutil import copyfile
from threading import Thread
import json

from TritonRacerSim.components.img_preprocessing import ImgPreprocessing
from TritonRacerSim.components.datastorage import DataStorage

import cv2

def post_process(source, destination, cfg={}):
    print("[Post-processing]")
    print(f'Source: {source}')
    print(f'Destination: {destination}')

    processor = ImgPreprocessing(cfg)
    t = Thread(target=processor.step_inputs, daemon=True)
    t.start()

    source = path.abspath(source)
    destination = path.abspath(destination)
    os.mkdir(destination)

    count = 0
    try: 
        while True:
            img = cv2.cvtColor(cv2.imread(path.join(source, f'img_{count}.jpg')), cv2.COLOR_BGR2RGB)
            processor.step(img,)
            copyfile(path.join(source, f'record_{count}.json'), path.join(destination, f'record_{count}.json'))
            while processor.processed_img is None:
                time.sleep(0.005)
            cv2.imwrite(path.join(destination, f'img_{count}.jpg'))
            processor.processed_img = None
            count += 1

    except FileNotFoundError:
        print(f'{count} records processed.')

def getImgPath(idx, parent):
    return path.join(parent, f'img_{idx}.jpg')

def getRecordPath(idx, parent):
    return path.join(parent, f'record_{idx}.json')

def shift_latency(source, destination):
    print("[Post-processing]")
    print(f'Source: {source}')
    print(f'Destination: {destination}')

    old_latency = int(input('What latency (ms) was these data trained with? Answer: '))
    new_latency = int(input('What is the new latency (ms)? Answer: '))
    if abs(old_latency - new_latency) <= 10:
        print('Latency less than 10ms cannot be shifted.')
        return
    idxShift = calcIdxShift(old_latency, new_latency)

    consent = input(f'The best we can do is to make the new latency {old_latency + idxShift * 20}. Do you accepct that? y/n')
    if consent.lower() == 'y':
        shiftIdx(source, destination, idxShift)
    else:
        print('User does not consent. Process aborted.')

def calcIdxShift(old, new):
    return math.ceil((new - old) / 20.0)

def shiftIdx(source, destination, amount):
    mkdir(path.abspath(destination))
    source = path.abspath(source)
    destination = path.abspath(destination)
    

    img_idx = 1
    record_idx = 1
    if amount > 0: # Delay the record
        record_idx += amount
    else:
        img_idx += amount

    count = 0
    try:
        while path.exists(getImgPath(img_idx, source)) and path.exists(getRecordPath(img_idx, source)):
            count += 1
            copyfile(getImgPath(img_idx, source), getImgPath(count, destination))
            copyfile(getRecordPath(record_idx, source), getRecordPath(count, destination))
            img_idx += 1
            record_idx += 1
            print(f'Processing {count} records...\r', end='')
        print(f'Finished processing {count} records.')

    except FileNotFoundError:
        print(f'Processed {count} records.')