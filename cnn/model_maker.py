import numpy as np
import keras

days_to_learn = 3700
days_given = 270
days_prediction = 60
ticker = 'AMZN'

data = np.load('./normalisation/data_sliced.npy')
data_norm = np.load('./normalisation/data_sliced_norm.npy')
to_predict = np.load('./normalisation/topredict.npy')

data = data[:, :, 1:]
data_norm = data_norm[:, : , 1:]
to_predict = to_predict - 1

print(to_predict)

n_cols = data_norm.shape[2]
entry_to_predict = 4404

data_to_predict = data_norm[entry_to_predict, 0:days_given, :]
data_to_predict = data_to_predict[np.newaxis, ...]
# data_to_predict = np.transpose(data_to_predict, (0, 2, 1))
print(data.shape)
print(data_to_predict.shape)
X = data_norm[:days_to_learn, 0:days_given, :]

for i in range(0, days_prediction):
    y = data_norm[:days_to_learn, days_given + i, to_predict]

    model = keras.Sequential()
    model.add(keras.layers.convolutional.Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(days_given, n_cols)))
    model.add(keras.layers.convolutional.Conv1D(filters=64, kernel_size=3, activation='relu', kernel_regularizer=keras.regularizers.L2(0.01)))
    model.add(keras.layers.convolutional.MaxPooling1D(pool_size=3))
    model.add(keras.layers.Dropout(rate=0.25))
    model.add(keras.layers.convolutional.Conv1D(filters=64, kernel_size=2, activation='relu', kernel_regularizer=keras.regularizers.L2(0.01)))
    model.add(keras.layers.convolutional.Conv1D(filters=64, kernel_size=2, activation='relu', kernel_regularizer=keras.regularizers.L2(0.01)))
    model.add(keras.layers.convolutional.MaxPooling1D(pool_size=2))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(128, activation='relu'))
    model.add(keras.layers.Dense(4))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs= 100)
    model.save('./cnn/'+ticker+'/'+str(i+1)+'.keras')

result = model.predict(data_to_predict)
print(result.shape)
print(result)

result_val = np.zeros((4))

for i in range(0, 4):
    result_val[i] = (result[0, i] - 1) * (np.max(data[entry_to_predict, :days_given, to_predict[i]]) - np.min(data[entry_to_predict, :days_given, to_predict[i]])) + np.min(data[entry_to_predict, :days_given, to_predict[i]])

print(data[entry_to_predict, days_given + i, [0,1]])
print(result_val) 