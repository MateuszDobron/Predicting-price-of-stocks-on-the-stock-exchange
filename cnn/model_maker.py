import numpy as np
import keras

days_to_learn = 3200
days_given = 500
days_prediction = 90

def make_model():
    data = np.load('./cnn/data/data_sliced.npy')
    data_norm = np.load('./cnn/data/data_sliced_norm.npy')
    to_predict = np.load('./cnn/data/topredict.npy')

    data = data[:, :, 1:]
    data_norm = data_norm[:, : , 1:]
    to_predict = to_predict - 1

    print(to_predict)
    print(to_predict.shape)

    n_cols = data_norm.shape[2]
    print(data.shape)

    X = data_norm[:days_to_learn, 0:days_given, :]
    y = np.zeros((days_to_learn, to_predict.shape[0] * days_prediction))

    for slice_number in range(0, days_to_learn):
        for indicator in range(0, to_predict.shape[0]):
            y[slice_number, indicator*days_prediction:(indicator+1)*days_prediction] = data_norm[slice_number, days_given:, to_predict[indicator]]

    print(y.shape)
    print(y[100, 1790:])
    print(data_norm[100, 580:, to_predict[19]])

    model = keras.Sequential()
    model.add(keras.layers.convolutional.Conv1D(filters=64, kernel_size=4, activation='relu', input_shape=(days_given, n_cols)))
    model.add(keras.layers.convolutional.Conv1D(filters=64, kernel_size=4, activation='relu', kernel_regularizer=keras.regularizers.L2(0.01)))
    model.add(keras.layers.convolutional.Conv1D(filters=64, kernel_size=4, activation='relu', kernel_regularizer=keras.regularizers.L2(0.01)))
    model.add(keras.layers.convolutional.MaxPooling1D(pool_size=4))
    model.add(keras.layers.Dropout(rate=0.4))
    model.add(keras.layers.convolutional.Conv1D(filters=64, kernel_size=3, activation='relu', kernel_regularizer=keras.regularizers.L2(0.01)))
    model.add(keras.layers.convolutional.Conv1D(filters=64, kernel_size=3, activation='relu', kernel_regularizer=keras.regularizers.L2(0.01)))
    model.add(keras.layers.convolutional.MaxPooling1D(pool_size=3))
    model.add(keras.layers.Dropout(rate=0.25))
    model.add(keras.layers.convolutional.Conv1D(filters=64, kernel_size=2, activation='relu', kernel_regularizer=keras.regularizers.L2(0.01)))
    model.add(keras.layers.convolutional.MaxPooling1D(pool_size=2))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(45000, activation='relu'))
    model.add(keras.layers.Dense(to_predict.shape[0] * days_prediction))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs= 20)
    model.save('./cnn/model.keras')
