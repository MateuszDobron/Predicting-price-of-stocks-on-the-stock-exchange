# Author: Piotr Cieślak

import csv
import keras.layers
import numpy
import pandas as pd
import logging
import datetime

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from numpy import array
# from pandas.tseries.holiday import get_calendar, HolidayCalendarFactory, GoodFriday

logging.getLogger().setLevel(logging.INFO)

class LSTMModel:
    # number of nodes used in the inner layers
    HID_LAYER_NODES_NUM = 15
    # number of nodes used in the output layer
    OUT_LAYER_NODES_NUM = 1
    # number of days, for which to predict the output price (size of input vector)
    INPUT_DAYS = 5
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
            keras.layers.LSTM(self.HID_LAYER_NODES_NUM, activation='tanh', return_sequences=True),
            keras.layers.LSTM(self.HID_LAYER_NODES_NUM, activation='tanh', return_sequences=False),
            keras.layers.Dense(self.OUT_LAYER_NODES_NUM)
        ])
        return model

    def load_model(self, model_path):
        self.model = keras.models.load_model(model_path) # load the model provided by user by given path
        self.INPUT_DAYS = self.model.layers[0].input_shape[1] # set the number of input days to be the same as the size of the input shape required by the model
        return keras.models.load_model(model_path)

    def train_model(self, file_path):
        logging.info('Started model training!')
        self.model.compile(loss='mse', optimizer='adam', metrics=['accuracy']) # compile the model using given parameters
        data_x, data_y = self.__prepare_train_data(file_path) # cut the training dataset into batches of size equal to the input size (data_x) and output size (data_y)
        #fixme delete return
        return self.model.fit(data_x, data_y, validation_split=0.33, epochs=100, verbose=2) # train the model

    def predict(self, prices):
        prices = prices.reshape(-1, 1)
        prices = self.__normalize_data(prices)
        prices = prices.reshape(1, -1)
        predicted_price = self.model.predict(prices, verbose=0)
        predicted_price_transformed = self.__inverse_transform(predicted_price)
        logging.info(f"Predicted price: {predicted_price_transformed[0]}")
        return predicted_price_transformed

    def predict_for_ticker(self, ticker):
        input = self.__extract_prediction_interval(ticker)
        predicted_price = self.predict(input[:,0])
        date = self.__extract_prediction_date(input[self.INPUT_DAYS - 1, 1:])

        return numpy.vstack([input, numpy.append(predicted_price, date)])

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
        delimiter = ',' # delimiter is a coma since data is stored in .csv (comma-separated values)
        if not file_path: # if user did not provide its own dataset for training then use the default dataset
            test_data = numpy.genfromtxt('../dataset/dataset.csv', delimiter=delimiter, usecols=7, dtype=float,
                                         skip_header=True, max_rows=3000) # loading of the default dataset, rows from 1 to 3000 are the training data
            test_data = test_data.reshape(-1, 1)
            test_data_normalized = self.__normalize_data(test_data) # normalize the data
            return self.extract_training_intervals(test_data_normalized) # extract batches of the desired size and return
        else: # if user provided its own dataset for training then use this dataset
            col_names_list = pd.read_csv(file_path, nrows=1, header=0).columns.to_list()

            # get index of column which contains close prices
            col_index = list(map(lambda col: 'close' in col.lower(), col_names_list)).index(True)

            data = numpy.genfromtxt(file_path, delimiter=delimiter, skip_header=1, usecols=col_index, dtype=float)
            print(data)

            data = data.reshape(-1, 1)
            data_normalized = self.__normalize_data(data)
            return self.extract_training_intervals(data_normalized)

    def extract_training_intervals(self, data):
        # data_input - prices from 5 days, data_output - price of the next day after 5 days
        data_input, data_exp_output = list(), list()
        for i in range(len(data)):
            end_ix = i + self.INPUT_DAYS # get the index of the last day in the sequence
            if end_ix > len(data) - 1:
                break
            seq_x, seq_y = data[i:end_ix], data[end_ix] # extract 5 days as the model input and the 6th day as the expected output
            data_input.append(seq_x)
            data_exp_output.append(seq_y)
        array_data_input, array_data_exp_output = array(data_input), array(data_exp_output)
        return array_data_input.reshape((array_data_input.shape[0], array_data_input.shape[1], 1)), \
            array_data_exp_output

    def __extract_prediction_interval(self, ticker):
        delimiter = ','
        input_data = list()
        with open(self.DEFAULT_DATASET, "r") as f:
            reader = csv.reader(f, delimiter=",")
            data = list(reader)
            row_count = len(data)
        col_names_list = pd.read_csv(self.DEFAULT_DATASET, nrows=1, header=0).columns.to_list()
        col_name = list(map(lambda col: ticker+'_Close' in col, col_names_list)).index(True) # get the column index of the company for which to perform predictions
        input_data = numpy.genfromtxt(self.DEFAULT_DATASET, skip_header=row_count-self.INPUT_DAYS, delimiter=delimiter, usecols=(col_name, 1, 2, 3), dtype=float) # usecols contains column which contains closing price for the company for which to perform prediction and date

        i = 1
        while numpy.isnan(input_data).any(): # if there is no value in any row in the input_data, shift one day earlier in the dataset
            input_data = numpy.genfromtxt(self.DEFAULT_DATASET, skip_header=row_count-self.INPUT_DAYS-i,
                                          max_rows=self.INPUT_DAYS, delimiter=delimiter, usecols=(col_name, 1, 2, 3),
                                          dtype=float)
            i += 1
        return input_data

    def __extract_prediction_date(self, prev_day_date):
        # extract the date for the predicted price to show on the graph
        date = datetime.datetime(int(prev_day_date[0]), int(prev_day_date[1]), int(prev_day_date[2]))
        if date.isoweekday() == 5: # if the day of the last known closing price is friday, then the next day on the stock must be monday, since the prices don't work on the weekends
            timedelta = 3
        else:
            timedelta = 1
        prediction_date = date + datetime.timedelta(days=timedelta)
        prediction_date_array = numpy.zeros((1,3))
        prediction_date_array[0][0] = prediction_date.year
        prediction_date_array[0][1] = prediction_date.month
        prediction_date_array[0][2] = prediction_date.day
        return prediction_date_array


    def __normalize_data(self, data):
        # perform normalization on given data
        self.data_scaler = self.scaler.fit(data)
        return self.data_scaler.transform(data)

    def __inverse_transform(self, data):
        # inverse transform the normalized data
        return self.data_scaler.inverse_transform(data)


# model = LSTMModel('')
# model.train_model('')
# model.save_model('C:\\dev\\git\\inzynierka\\lstm_model\\saved_models\\model.keras')
# x_input = array([122, 124, 119])
# x_input = x_input.reshape((1, 3, 1))
# print(model.predict(x_input))
# print(model.predict_for_given_days(x_input, 3))