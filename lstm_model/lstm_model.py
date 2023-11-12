import csv

import keras.layers
import numpy
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from numpy import array


class LSTMModel:
    # number of nodes used in the inner layers
    HID_LAYER_NODES_NUM = 10
    # number of nodes used in the output layer
    OUT_LAYER_NODES_NUM = 1
    # number of days, for which to predict the output price (size of input vector)
    INPUT_DAYS = 3
    # number of predicted days (size of output vector)
    OUTPUT_DAYS = 1
    # default training/prediction dataset file path
    DEFAULT_DATASET = '../dataset/dataset.csv'
    # MinMax scaler for data normalization
    scaler = MinMaxScaler()
    data_scaler = None

    def __init__(self, model_path):
        if not model_path:
            self.model = self.init_model()
        else:
            self.model = self.load_model(model_path)

    def init_model(self):
        # input shape 3,1 because we take previous 3 days and predict the one (the next) day
        model = Sequential([
            keras.layers.LSTM(self.HID_LAYER_NODES_NUM, activation='relu', input_shape=(self.INPUT_DAYS, 1),
                              return_sequences=True),
            keras.layers.LSTM(self.HID_LAYER_NODES_NUM, activation='tanh', return_sequences=True),
            keras.layers.LSTM(self.HID_LAYER_NODES_NUM, activation='tanh', return_sequences=True),
            keras.layers.LSTM(self.HID_LAYER_NODES_NUM, activation='tanh', return_sequences=False),
            keras.layers.Dense(self.OUT_LAYER_NODES_NUM)
        ])
        return model

    def load_model(self, model_path):
        return keras.models.load_model(model_path)

    def train_model(self, file_path):
        self.model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
        data_x, data_y = self.__prepare_train_data(file_path)
        self.model.fit(data_x, data_y, epochs=10, verbose=1)

    def predict(self, prices):
        prices = prices.reshape(-1, 1)
        prices = self.__normalize_data(prices)
        prices = prices.reshape(1, -1)
        predicted_price = self.model.predict(prices, verbose=0)
        return self.__inverse_transform(predicted_price)

    def predict(self, ticker):
        input = self.__extract_prediction_prices(ticker)
    def predict_for_given_days(self, prices, num_of_days):
        predicted_prices = numpy.empty(num_of_days, dtype=float)
        model_input = prices
        for i in range(num_of_days):
            predicted_price = self.predict(model_input)
            predicted_prices[i] = predicted_price
            model_input[0] = model_input[1]
            model_input[1] = model_input[2]
            model_input[2] = predicted_price
        print(predicted_prices)
        return predicted_prices

    def save_model(self, path):
        self.model.save(path)

    def __prepare_train_data(self, file_path):
        delimiter = ','
        if not file_path:
            test_data = numpy.genfromtxt('../dataset/dataset.csv', delimiter=delimiter, usecols=7, dtype=float,
                                         skip_header=True, max_rows=251)
            test_data = test_data.reshape(-1, 1)
            return self.__extract_training_intervals(test_data)
        else:
            col_names_list = pd.read_csv(file_path, nrows=1, header=0).columns.to_list()

            # get index of column which contains close prices
            col_index = list(map(lambda col: 'close' in col, col_names_list)).index(True)

            data = numpy.genfromtxt(file_path, delimiter=delimiter, skip_header=1, usecols=col_index, dtype=float)
            print(data)

            data = data.reshape(-1, 1)
            data_normalized = self.__normalize_data(data)
            return self.__extract_training_intervals(data_normalized)

    def __extract_training_intervals(self, data):
        # data_input - prices from 3 days, data_output - price of the next day after 3 days
        data_input, data_exp_output = list(), list()
        for i in range(len(data)):
            end_ix = i + self.INPUT_DAYS
            if end_ix > len(data) - 1:
                break
            seq_x, seq_y = data[i:end_ix], data[end_ix]
            data_input.append(seq_x)
            data_exp_output.append(seq_y)
        array_data_input, array_data_exp_output = array(data_input), array(data_exp_output)
        return array_data_input.reshape((array_data_input.shape[0], array_data_input.shape[1], 1)), \
            array_data_exp_output

    def __extract_prediction_interval(self, ticker):
        data_input = list()
        with open('filename', "r") as f:
            reader = csv.reader(f, delimiter=",")
            data = list(reader)
            row_count = len(data)


    def __normalize_data(self, data):
        self.data_scaler = self.scaler.fit(data)
        return self.data_scaler.transform(data)

    def __inverse_transform(self, data):
        return self.data_scaler.inverse_transform(data)


model = LSTMModel('')
# model.train_model('C:\\Users\\piotr\\PycharmProjects\\group_project\\lstm_model\\datasets\\nasdaq.csv')
# model.save_model('C:\\Users\\piotr\\PycharmProjects\\group_project\\lstm_model\\saved_models\\model.keras')
model.train_model('')
x_input = array([122, 124, 119])
# x_input = x_input.reshape((1, 3, 1))
print(model.predict(x_input))
#print(model.predict_for_given_days(x_input, 3))