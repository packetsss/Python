'''Converts keras model to onnx format'''
import keras2onnx
from tensorflow.keras.models import load_model
from os import path
import onnx

keras_model_name = 'localization.h5'
onnx_model_name = 'localization_keras.onnx'

model = load_model(path.abspath(keras_model_name))
onnx_model = keras2onnx.convert_keras(model, model.name)
onnx.save_model(onnx_model, onnx_model_name)