import numpy as np
import tensorflow as tf
import pandas as pd

MSFT_pos = [2, 3, 4, 5]
AAPL_pos = [18, 19, 20, 21]
# Open, High, Low, Close
days_given = 270
days_prediction = 60

def run(data, data_to_predict, ticker, result_pos):
    
    result = np.zeros((days_prediction, 4))

    for i in range(0, days_prediction):
        model = tf.keras.models.load_model('./cnn/' + ticker + '/' + str(i + 1) + '.keras')
        prediction = model(data_to_predict)
        for j in range(0, 4):
            result[i, j] = (prediction[0, j] - 1) * (np.max(data[:days_given, result_pos[j]]) - np.min(data[:days_given, result_pos[j]])) + np.min(data[:days_given, result_pos[j]])

    return result
