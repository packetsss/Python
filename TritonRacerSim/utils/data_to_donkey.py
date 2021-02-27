from os import path
import os
import json
from PIL import Image

source = '/home/haoru/Projects/Triton-Racer/Triton-Racer-Sim/TritonRacerSim/car_templates/data/records_1/'
destination = '/home/haoru/Projects/Donkeys/Custom/d_custom/data/records_1/'
os.mkdir(destination)

i = 1
while True:
    try:
        input_img_path = path.join(source, f'img_{i}.jpg')
        input_record_path = path.join(source, f'record_{i}.json')

        output_img_path = path.join(destination, f'{i}_cam-image_array_.jpg')
        output_record_path = path.join(destination, f'record_{i}.json')

        img = Image.open(input_img_path)
        img.save(output_img_path)

        with open(input_record_path) as f:
            record = json.load(f)
        output_record = {"cam/image_array": f'{i}_cam-image_array_.jpg',
                        "user/angle": record['mux/steering'],
                        "user/throttle": record['mux/throttle'],
                        "user/mode": "user",
                        "milliseconds": i}
        with open(output_record_path, 'w') as f:
            json.dump(output_record, f)

        i += 1

    except FileNotFoundError:
        print(f'{i} records converted.')
        break
