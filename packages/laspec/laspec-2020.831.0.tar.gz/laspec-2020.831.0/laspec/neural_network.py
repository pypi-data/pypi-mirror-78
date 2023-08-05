# %%%% code
from tensorflow import keras
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, BatchNormalization, Input
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import Conv1D, GlobalMaxPooling1D, MaxPooling1D, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.datasets import imdb
from tensorflow.keras.optimizers import RMSprop, SGD, Adam
from tensorflow.keras import backend as K
from tensorflow.keras import losses
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import load_model
import os
import joblib
import numpy as np
from sklearn.model_selection import train_test_split


def set_gpu(device="1"):
    os.environ["CUDA_VISIBLE_DEVICES"] = device
    return


xtrain, xtest, ytrain, ytest = train_test_split(fluxb, pbs, test_size=20000, random_state=0)


class EzNN():
    """ simple one-hidden-layer NN """
    model = None

    def __init__(self, ns):
        self.ns = ns
        self.msh
        pass

    @staticmethod
    def create_c2nn(ns=(2, 100, 1)):
        model = Sequential()
        model.add(Dense(ns[1], activation="sigmoid", input_shape=(ns[0], 1)))  # input_shape=(4000,)
        model.add(BatchNormalization())
        model.add(Dropout(0.2))
        model.add(Dense(ns[2], activation="sigmoid"))
        return model

    def ezpredict(self, x):



def test_eznn():
    x = np.random.uniform(-.5, .5, 10000)
    x.sort()
    y = np.sin(50*x)


# %% parameterization
def train(model, opt, epochs, initial_epoch=0, mcp=None):
    model.compile(optimizer=opt,
                  loss='mse',
                  metrics=['mae'])
    # model.summary()
    # #%%
    history = model.fit(xtrain[:, :npixB].reshape(*xtrain[:, :npixB].shape, 1),
                        ytrain.reshape(*ytrain.shape, 1),
                        batch_size=128,
                        epochs=epochs,
                        initial_epoch=initial_epoch,
                        callbacks=mcp,
                        validation_data=(xtest[:, :npixB].reshape(*xtest[:, :npixB].shape, 1),
                                         ytest.reshape(*ytest.shape, 1)))
    return history

filepath = "../data/v10mcp/v10_param_{epoch:04d}_{loss:0.6f}_{val_loss:0.6f}.hdf5"
mcp = ModelCheckpoint(filepath, monitor="val_accuracy", verbose=1)
npixB = np.sum(waveBR < 5500)
# npixB=1000
model = create_c2nn(ninput=npixB)
model.summary()
history = train(model, Adam(lr=1e-5), epochs=200, mcp=mcp)
