import numpy as np
import tensorflow as tf
import pandas as pd
import numpy as np

days_given = 500
days_prediction = 90
data = np.load('./cnn/data/data_sliced.npy')
data_norm = np.load('./cnn/data/data_sliced_norm.npy')
to_predict = np.load('./cnn/data/topredict.npy')
to_normalize = np.load('./cnn/data/tonormalize.npy')
to_normalize = to_normalize - 1
to_predict = to_predict - 1
data = data[:, :, 1:]
data_norm = data_norm[:, : , 1:]

def make_prediction():
    X = data[data.shape[0] - 1, days_prediction:, :]
    X_norm = X.copy()
    print(X.shape)
    print(to_normalize)
    for column in to_normalize:
            if(np.max(X[:, column]) - np.min(X[:, column]) == 0):
                X_norm[:, column] = 1.5
            else:
                X_norm[:, column] = (X[:, column] - np.min(X[:, column])) / (np.max(X[:, column]) - np.min(X[:, column])) + 1

    model = tf.keras.models.load_model('./cnn/model.keras')
    X_norm = X_norm[np.newaxis, ...]
    prediction = model(X_norm)
    result = np.zeros((days_prediction, to_predict.shape[0]))
    for indicator in range(0, to_predict.shape[0]):
        result[:, indicator] = prediction[0, (indicator * days_prediction):((indicator + 1) * days_prediction)] - 1
        result[:, indicator] = (result[:, indicator]) * (np.max(X[:, to_predict[indicator]]) - np.min(X[:, to_predict[indicator]])) + np.min(X[:, to_predict[indicator]])
    return result
