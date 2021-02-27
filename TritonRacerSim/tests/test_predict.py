from tensorflow.python.keras.models import load_model
import tensorflow as tf
from os import path
from PIL import Image
import numpy as np
import time
import os
# os.environ["CUDA_VISIBLE_DEVICES"]="-1"
model_path = path.abspath('./models/race4.h5')


model = load_model(model_path, compile=False)
tf.keras.backend.set_learning_phase(0)

for i in range(6, 20):
    img_path = path.abspath('./data/records_1/img_{}.jpg'.format(i))
    img = Image.open(img_path)
    img_arr = np.asarray(img)
    img_arr = img_arr.reshape((1,) + img_arr.shape)
    start_time = time.time()
    steering, throttle = model(img_arr)
    print (steering.numpy()[0][0], throttle.numpy()[0][0])
    print(f'Prediction time: {time.time() - start_time}')

