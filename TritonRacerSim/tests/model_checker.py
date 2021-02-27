from tensorflow.python.keras.models import load_model
import tensorflow as tf
from os import path

# model = load_model('./models/race1-1.h5')
# model.summary()

model_path = './race4c.h5'
model = load_model(path.abspath(model_path))
model.summary()