
from os import path
import numpy as np
from PIL import Image
import json
from enum import Enum
import time
import os

import tensorflow as tf
from tensorflow.keras.layers.experimental.preprocessing import Rescaling
from tensorflow.keras.layers import Input, Conv2D, Dense, Dropout, Flatten, Concatenate
from tensorflow.keras import optimizers, losses
from tensorflow.keras.models import Model
from tensorflow.python.keras.models import load_model
from tensorflow.keras import layers

from TritonRacerSim.components.controller import DriveMode
from TritonRacerSim.utils.types import ModelType
from TritonRacerSim.components.component import Component

class DataLoader:
    '''Load img and json records from record folder'''
    def __init__(self, *paths):
        self.paths = paths
        for data_path in paths:
            if not path.exists(data_path):
                raise FileNotFoundError(f'Folder does not exists: {data_path}')
        self.dataset = []
        self.train_dataset = None
        self.val_dataset = None

    def load(self, train_val_split = 0.8, batch_size = 128):
        print ('Loading records...')
        for data_path in self.paths:
            i = 1
            while True:
                try:
                    # Obtain img as array
                    img_path = path.join(data_path, self.get_img_name(i))
                    img_arr = np.asarray(Image.open(img_path),dtype=np.float32)
                    img_arr /= 255

                    # Obtain labels and feature vectors as arrays
                    record_path = path.join(data_path, self.get_record_name(i))
                    record={}
                    with open(record_path) as f:
                        record= json.load(f)
                    labels = np.asarray(self.get_labels_from_record(record),dtype=np.float32)
                    feature_vectors = np.asarray(self.get_features_from_record(record), dtype=np.float32)

                    self.dataset.append((img_arr, feature_vectors, labels))
                    # print (labels)
                    i += 1
                except FileNotFoundError:
                    # print (f'Loaded {i-1} records in {data_path}')
                    break

        print (f'Loaded {len(self.dataset)} records.')
        self.__split_train_val(train_val_split)

        SHUFFLE_BUFFER_SIZE = 5000
        self.train_dataset_batch = self.train_dataset.unbatch().shuffle(SHUFFLE_BUFFER_SIZE).batch(batch_size, drop_remainder=True)
        self.val_dataset_batch = self.val_dataset.unbatch().shuffle(SHUFFLE_BUFFER_SIZE).batch(batch_size, drop_remainder=True)

    def __split_train_val(self, split = 0.8):
        assert 0 < split <= 1
        from sklearn.model_selection import train_test_split
        train_set, val_set = train_test_split(self.dataset, train_size = split)

        train_examples = []
        train_example_vecs = []
        train_labels = []

        val_examples = []
        val_example_vecs = []
        val_labels = []
        
        for data in train_set:
            if data[1].size: #Has feature vectors?
                train_examples.append(data[0])
                train_example_vecs.append(data[1])
            else:
                train_examples.append(data[0])
            train_labels.append(data[2])

        for data in val_set:
            val_examples.append(data[0])
            if data[1].size:
                val_example_vecs.append(data[1])
            val_labels.append(data[2])

        train_examples = np.stack(train_examples, axis=0)
        train_labels = np.stack(train_labels, axis=0)
        val_examples = np.stack(val_examples, axis=0)
        val_labels = np.stack(val_labels, axis=0)

        if train_example_vecs:
            train_example_vecs = np.stack(train_example_vecs, axis=0)
            val_example_vecs = np.stack(val_example_vecs, axis=0)
            self.train_dataset = tf.data.Dataset.from_tensors(((train_examples, train_example_vecs), train_labels))
            self.val_dataset = tf.data.Dataset.from_tensors(((val_examples, val_example_vecs), val_labels)) 
        else:
            self.train_dataset = tf.data.Dataset.from_tensors((train_examples, train_labels))
            self.val_dataset = tf.data.Dataset.from_tensors((val_examples, val_labels))        

    def get_img_name(self, idx):
        return f'img_{idx}.jpg'

    def get_record_name(self, idx):
        return f'record_{idx}.json'

    def get_labels_from_record(self, record={}):
        return record['mux/steering'], record['mux/throttle'] # Adjust the input range to be [0, 1]

    def get_features_from_record(self,record={}):
        '''Any additional features are we looking for?'''
        # return record['gym/speed'], record['gym/cte']
        return None
    

class Keras_2D_CNN(Component):
    '''2D CNN models'''
    def __init__(self, input_shape, num_outputs, num_feature_vectors = 0):
        pass
    
    @staticmethod
    def get_model(input_shape, num_outputs, num_feature_vectors = 0):
        inputs = Input(shape=input_shape, name='img_input')
        
        drop = 0.1

        # x = Rescaling(scale=1.0/255)(inputs)
        x = Conv2D(filters=24, kernel_size=(5, 5), strides=(2,2),activation='relu', name='conv1')(inputs)
        x = Dropout(drop)(x)
        x = Conv2D(filters=32, kernel_size=(5, 5), strides=(2,2),activation='relu', name='conv2')(x)
        x = Dropout(drop)(x)
        x = Conv2D(filters=64, kernel_size=(5, 5), strides=(2,2),activation='relu', name='conv3')(x)
        x = Dropout(drop)(x)
        x = Conv2D(filters=64, kernel_size=(3, 3), strides=(1,1),activation='relu', name='conv4')(x)
        x = Dropout(drop)(x)
        x = Conv2D(filters=64, kernel_size=(3, 3), strides=(1,1),activation='relu', name='conv5')(x)
        x = Dropout(drop)(x)
        
        x = Conv2D(filters=128, kernel_size=(3, 3), strides=(1,1),activation='relu', name='conv6')(x)
        x = Dropout(drop)(x)
        x = Conv2D(filters=128, kernel_size=(3, 3), strides=(1,1),activation='relu', name='conv7')(x)
        x = Dropout(drop)(x)
        x = Flatten(name='flatten1')(x)
        z = x
        if num_feature_vectors > 0:
            feature_inputs = Input(shape=(num_feature_vectors,), name='feature_vec_input')
            y = Dense(num_feature_vectors * 4, activation='relu', name='feature1')(feature_inputs)
            y = Dense(num_feature_vectors * 8, activation='relu', name='feature2')(y)
            y = Dense(num_feature_vectors * 16, activation='relu', name='feature3')(y)
            z = Concatenate(axis=1)([x, y])
        
        z = Flatten(name='flatten2')(z)
        z = Dense(100, activation='relu', name = 'dense1')(z)
        z = Dropout(drop)(z)
        z = Dense(50, activation='relu', name = 'dense2')(z)
        z = Dropout(drop)(z)      
        z = Dense(25, activation='relu', name = 'dense3')(z)
        z = Dropout(drop)(z)
        

        outputs = Dense(num_outputs, activation='linear', name='output_layer')(z)
            
        if num_feature_vectors > 0:
            model = Model(inputs=[inputs, feature_inputs], outputs=[outputs])
        else:
            model = Model(inputs=[inputs], outputs=[outputs])
        
        return model

class Keras_2D_FULL_HOUSE(Component):
    '''
    Inputs: image, current speed, track localization, track offset
    Outputs: steering, best speed
    '''
    def __init__(self, input_shape, num_outputs, num_feature_vectors = 0):
        pass
    
    @staticmethod
    def get_model(input_shape):
        inputs = Input(shape=input_shape, name='img_input')
        
        drop = 0.1

        x = Conv2D(filters=24, kernel_size=(5, 5), strides=(2,2),activation='relu', name='conv1')(inputs)
        x = Dropout(drop)(x)
        x = Conv2D(filters=32, kernel_size=(5, 5), strides=(2,2),activation='relu', name='conv2')(x)
        x = Dropout(drop)(x)
        x = Conv2D(filters=64, kernel_size=(5, 5), strides=(2,2),activation='relu', name='conv3')(x)
        x = Dropout(drop)(x)
        x = Conv2D(filters=64, kernel_size=(3, 3), strides=(1,1),activation='relu', name='conv4')(x)
        x = Dropout(drop)(x)
        x = Conv2D(filters=64, kernel_size=(3, 3), strides=(1,1),activation='relu', name='conv5')(x)
        x = Dropout(drop)(x)
        
        x = Conv2D(filters=128, kernel_size=(3, 3), strides=(1,1),activation='relu', name='conv6')(x)
        x = Dropout(drop)(x)
        x = Conv2D(filters=128, kernel_size=(3, 3), strides=(1,1),activation='relu', name='conv7')(x)
        x = Dropout(drop)(x)
        x = Flatten(name='flatten1')(x)



        feature_inputs = Input(shape=(1,), name='feature_vec_input')
        y = Dense(16, activation='relu', name='feature1')(feature_inputs)
        y = Dense(32, activation='relu', name='feature2')(y)
        y = Dense(64, activation='relu', name='feature3')(y)

        x = Concatenate(axis=1)([x, y])
      
        z = Flatten(name='flatten2')(x)
        z = Dense(100, activation='relu', name = 'dense1')(z)
        z = Dropout(drop)(z)
        z = Dense(50, activation='relu', name = 'dense2')(z)
        z = Dropout(drop)(z)      
        z = Dense(25, activation='relu', name = 'dense3')(z)
        z = Dropout(drop)(z)
        
        out_speed = Dense(1, activation='linear', name='output_speed')(z)

        current_spd_input = Input(shape=(1,), name='current_spd_input')
        s = Dense(16, activation='relu', name='current_spd_1')(current_spd_input)
        s = Dense(32, activation='relu', name='current_spd_2')(s)
        s = Dense(64, activation='relu', name='current_spd_3')(s)
        
        s = Concatenate(axis=1)([x,s])
        s = Dense (100, activation='relu', name = 'dense4')(s)
        s = Dropout(drop)(s)
        s = Dense(50, activation='relu', name = 'dense5')(s)
        s = Dropout(drop)(s) 
        s = Dense(25, activation='relu', name = 'dense6')(s)
        s = Dropout(drop)(s)

        out_steering = Dense(1, activation='linear', name='out_steering')(s)

        outputs = Concatenate(axis=1)([out_steering, out_speed])
            
        model = Model(inputs=[inputs, current_spd_input, feature_inputs], outputs=[outputs])
        
        return model

class DonkeyDataLoader(DataLoader):
    def __init__(self, *paths):
        DataLoader.__init__(self, *paths)
    def get_img_name(self, idx):
        return f'{idx}_cam-image_array_.jpg'

    def get_record_name(self, idx):
        return f'record_{idx}.json'

    def get_labels_from_record(self, record={}):
        return np.asarray((record['user/angle'], record['user/throttle']))

    def get_features_from_record(self,record={}):
        '''Any additional features are we looking for?'''
        # return record['gym/speed'], record['gym/cte']
        return None
    
class SpeedFeatureDataLoader(DataLoader):
    def __init__(self, *paths):
        DataLoader.__init__(self, *paths)
    def get_features_from_record(self,record={}):
        '''Any additional features are we looking for?'''
        return np.asarray((record['gym/speed'] / 20,))
    
class SpeedCtlDataLoader(DataLoader):
    def __init__(self, *paths):
        DataLoader.__init__(self, *paths)

    def get_labels_from_record(self, record={}):
        return np.asarray((record['mux/steering'], record['gym/speed'] / 20)) # Adjust the input range to be [0, 1]
    
class LocalizationDemoDataLoader(DataLoader):
    def __init__(self, *paths):
        DataLoader.__init__(self, *paths)
    def get_img_name(self, idx):
        return f'record_{idx}.png'

    def get_record_name(self, idx):
        return f'record_{idx}.json'

    def get_labels_from_record(self, record={}):
        return np.asarray((record['x'] / 20, record['y'] / 20, record['orientation'] / 360), dtype=np.float16) # Adjust the input range to be [0, 1]
    
class FullHouseDataLoader(DataLoader):
    def __init__(self, *paths):
        DataLoader.__init__(self, *paths)
    
    def get_features_from_record(self,record={}):
        '''Any additional features are we looking for?'''
        return np.asarray((record['gym/speed'] / 20, record['loc/segment']))
    
    def get_labels_from_record(self, record={}):
        return np.asarray((record['mux/steering'], record['gym/speed'] / 20))

    def load(self, train_val_split = 0.8, batch_size = 128):
        print ('Loading records...')
        for data_path in self.paths:
            i = 1
            while True:
                try:
                    # Obtain img as array
                    img_path = path.join(data_path, self.get_img_name(i))
                    img_arr = np.asarray(Image.open(img_path),dtype=np.float32)
                    img_arr /= 255

                    # Obtain labels and feature vectors as arrays
                    record_path = path.join(data_path, self.get_record_name(i))
                    record={}
                    with open(record_path) as f:
                        record= json.load(f)
                    labels = np.asarray(self.get_labels_from_record(record),dtype=np.float32)
                    feature_vectors = np.asarray(self.get_features_from_record(record), dtype=np.float32)

                    self.dataset.append((img_arr, feature_vectors, labels))
                    # print (labels)
                    i += 1
                except FileNotFoundError:
                    # print (f'Loaded {i-1} records in {data_path}')
                    break

        print (f'Loaded {len(self.dataset)} records.')
        self.__split_train_val(train_val_split)

        SHUFFLE_BUFFER_SIZE = 5000
        self.train_dataset_batch = self.train_dataset.unbatch().shuffle(SHUFFLE_BUFFER_SIZE).batch(batch_size, drop_remainder=True)
        self.val_dataset_batch = self.val_dataset.unbatch().shuffle(SHUFFLE_BUFFER_SIZE).batch(batch_size, drop_remainder=True)
    
    def __split_train_val(self, split = 0.8):
        assert 0 < split <= 1
        from sklearn.model_selection import train_test_split
        train_set, val_set = train_test_split(self.dataset, train_size = split)

        train_examples = []
        train_example_spds = []
        train_example_vecs = []
        train_labels = []

        val_examples = []
        val_example_spds = []
        val_example_vecs = []
        val_labels = []
        
        for data in train_set:
            train_examples.append(data[0])
            train_example_vecs.append(np.asarray(data[1][1]))
            train_example_spds.append(np.asarray(data[1][0]))
            train_labels.append(data[2])

        for data in val_set:
            val_examples.append(data[0])
            val_example_spds.append(np.asarray(data[1][0]))
            val_example_vecs.append(np.asarray(data[1][1]))
            val_labels.append(data[2])

        train_examples = np.stack(train_examples, axis=0)
        train_labels = np.stack(train_labels, axis=0)
        train_example_vecs = np.stack(train_example_vecs, axis=0)
        train_example_spds = np.stack(train_example_spds, axis=0)

        val_examples = np.stack(val_examples, axis=0)
        val_labels = np.stack(val_labels, axis=0)
        val_example_vecs = np.stack(val_example_vecs, axis=0)
        val_example_spds = np.stack(val_example_spds, axis=0)

        self.train_dataset = tf.data.Dataset.from_tensors(((train_examples, train_example_spds, train_example_vecs), train_labels))
        self.val_dataset = tf.data.Dataset.from_tensors(((val_examples,val_example_spds, val_example_vecs), val_labels)) 



def train(cfg, data_paths, model_path, transfer_path=None):
    physical_devices = tf.config.list_physical_devices('GPU')
    if physical_devices:
        tf.config.experimental.set_memory_growth(physical_devices[0], True)

    loader = None
    model = None

    model_type = ModelType(cfg['model_type'])
    input_shape = (cfg['img_h'], cfg['img_w'], 3)

    if model_type == ModelType.CNN_2D:
        loader = DataLoader(*data_paths)
        model = Keras_2D_CNN.get_model(input_shape=input_shape, num_outputs=2, num_feature_vectors=0)
    elif model_type == ModelType.CNN_2D_SPD_FTR:
        loader = SpeedFeatureDataLoader(*data_paths)
        model = Keras_2D_CNN.get_model(input_shape=input_shape,num_outputs=2, num_feature_vectors=1)
    elif model_type == ModelType.CNN_2D_SPD_CTL:
        loader = SpeedCtlDataLoader(*data_paths)
        model = Keras_2D_CNN.get_model(input_shape=input_shape, num_outputs=2, num_feature_vectors=0)
    elif model_type == ModelType.CNN_2D_FULL_HOUSE:
        loader = FullHouseDataLoader(*data_paths)
        model = Keras_2D_FULL_HOUSE.get_model(input_shape=input_shape)

    if transfer_path is not None:
        model = load_model(transfer_path)
    loader.load(batch_size=cfg['batch_size'])
    model.summary()
    model.compile(optimizer=optimizers.Adam(lr=0.001), loss='mse')

    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(filepath=model_path, save_best_only=True, monitor='val_loss', mode='auto', verbose=1, save_freq='epoch')
    ]

    if cfg['early_stop']:
        callbacks.append(tf.keras.callbacks.EarlyStopping(patience=cfg['early_stop_patience']))

    model.fit(loader.train_dataset_batch, epochs=cfg['max_epoch'], validation_data=loader.val_dataset_batch, callbacks=callbacks)
    print(f'Finished training. Best model saved to {model_path}.')
    # model.save(model_path)

 



