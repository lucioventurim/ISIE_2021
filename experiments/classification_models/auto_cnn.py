# CNN

from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np
import os
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

def sig_image(data,size):
    X=np.zeros((data.shape[0],size,size))
    for i in range(data.shape[0]):
        X[i]=(data[i,:].reshape(size,size))
    return X.astype(np.float16)


class CNN(BaseEstimator, ClassifierMixin):
    def __init__(self,
                 kernel_size=32,
                 filters=32,
                 optimizer='adam',
                 epochs=100
                 ):
        self.kernel_size = kernel_size
        self.filters = filters
        self.optimizer = optimizer
        self.epochs = epochs
        self.n_features = 1

    def fit(self, X, y=None):
        kernel_size = self.kernel_size
        filters = self.filters
        optimizer = self.optimizer
        epochs = self.epochs

        #x_n = sig_image(X, 50)
        #print(x_n)
        #print(x_n.shape)


        # Define input shapes
        #self.n_samples = X.shape[0]
        self.n_steps = X.shape[1]

        X = X.reshape((X.shape[0], X.shape[1], self.n_features))
        #x_n = x_n.reshape((x_n.shape[0], x_n.shape[1], x_n.shape[2], self.n_features))

        self.labels, ids = np.unique(y, return_inverse=True)
        y_cat = to_categorical(ids)
        num_classes = y_cat.shape[1]

        self.model = Sequential()
        self.model.add(layers.InputLayer(input_shape=(self.n_steps, self.n_features)))
        self.model.add(layers.Conv1D(100, 6, activation='relu'))
        self.model.add(layers.Conv1D(100, 6, activation='relu'))
        self.model.add(layers.MaxPooling1D(3))
        self.model.add(layers.Conv1D(160, 6, activation='relu'))
        self.model.add(layers.Conv1D(160, 6, activation='relu'))
        self.model.add(layers.GlobalAveragePooling1D(name='G_A_P_1D'))
        self.model.add(layers.Dropout(0.5))
        self.model.add(layers.Dense(num_classes))
        self.model.add(layers.Activation('softmax'))
        self.model.compile(loss='categorical_crossentropy',
                           optimizer=optimizer,
                           metrics=["categorical_accuracy"])
        self.model.fit(X, y_cat, epochs=epochs, verbose=False)

        """
        self.model = Sequential()
        #self.model.add(layers.InputLayer(input_shape=(self.n_steps, self.n_features)))
        self.model.add(layers.InputLayer(input_shape=(self.n_steps, self.n_steps, self.n_features)))
        self.model.add(layers.Conv2D(32, (3, 3), activation="relu", strides=1))
        self.model.add(layers.MaxPooling2D(pool_size=(2, 2), strides=1))
        self.model.add(layers.Conv2D(64, (3, 3), activation="relu", strides=1))
        self.model.add(layers.MaxPooling2D(pool_size=(2, 2), strides=1))
        #self.model.add(layers.MaxPooling2D(pool_size=(2,2), strides=(2,2)))
        self.model.add(layers.Conv2D(128, (3, 3), activation="relu", strides=1))
        self.model.add(layers.MaxPooling2D(pool_size=(2, 2), strides=1))
        self.model.add(layers.Dense(160, activation='relu'))
        self.model.add(layers.Dense(80, activation='relu'))
        self.model.add(layers.Flatten())
        self.model.add(layers.Dense(num_classes))
        self.model.add(layers.Activation('softmax'))
        self.model.compile(loss='categorical_crossentropy',
                           optimizer=optimizer,
                           metrics=["categorical_accuracy"])
        self.model.fit(x_n, y_cat, epochs=epochs, verbose=False)
        """


    def predict_proba(self, X, y=None):
        X = X.reshape((X.shape[0], X.shape[1], self.n_features))
        #X = sig_image(X, 50)
        #X = X.reshape((X.shape[0], X.shape[1], X.shape[2], self.n_features))
        return self.model.predict(X)

    def predict(self, X, y=None):
        X = X.reshape((X.shape[0], X.shape[1], self.n_features))
        #X = sig_image(X, 50)
        #X = X.reshape((X.shape[0], X.shape[1], X.shape[2], self.n_features))
        predictions = self.model.predict(X)
        return self.labels[np.argmax(predictions, axis=1)]


def instantiate_auto_cnn():

    cnn = CNN()

    return cnn
