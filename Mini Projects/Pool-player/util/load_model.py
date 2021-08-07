import numpy as np
from .settings import DECODER_DICT
import tensorflow as tf
from tensorflow.keras import layers as L
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import RMSprop

class Model:
    def __init__(self):
        self.num_classes = 4

        self.model = Sequential()
        self.model.add(tf.keras.layers.experimental.preprocessing.Rescaling(1./255))
        self.model.add(tf.keras.applications.resnet50.ResNet50(input_shape = (75, 75, 3),
                                        pooling = 'avg',
                                        include_top = False, 
                                        weights = 'imagenet'))

        self.model.add(L.Flatten())
        self.model.add(L.Dense(128, activation='relu'))
        self.model.add(L.Dense(self.num_classes, activation='softmax'))

        self.model.compile(optimizer=RMSprop(learning_rate=0.0001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    def load(self, path):
        self.model.load_weights(path)
    
    def predict(self, img, expand_img=True):
        if expand_img:
            img = np.expand_dims(img, axis=0)
            return DECODER_DICT[np.argmax(self.model.predict(img))]
        
        return self.model.predict(img)
