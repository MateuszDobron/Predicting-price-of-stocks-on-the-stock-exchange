import numpy as np
import keras

days_given = 180
days_prediction = 60

data = np.load('./normalisation/data_sliced.npy')
data_norm = np.load('/normalisation/data_sliced_norm.npy')



model = keras.Sequential([keras.Conv1D(100, kernel_size=3, )])