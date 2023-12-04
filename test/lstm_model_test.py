import unittest
import random
import numpy as np
from lstm_model.lstm_model import LSTMModel
class LstmModelTest(unittest.TestCase):

    def test_extracting_training_intervals(self):
        '''' Test whether extracting training intervals works correctly'''
        data = self.prepare_test_data()
        model = LSTMModel('')
        data_extracted = model.extract_training_intervals(data)
        for i in range(0, len(data_extracted[1])):
            self.assertEqual(data[i+model.INPUT_DAYS], data_extracted[1][i])
            for j in range(0, model.INPUT_DAYS):
                self.assertEqual(data[i+j], data_extracted[0][i][j])


    def test_normalize_data(self):
        ''' Test of data normalization and inverse transforming the data later '''
        model = LSTMModel('')
        data = self.prepare_test_data()
        data_reshaped = data.reshape(-1, 1)
        data_normalized = model._LSTMModel__normalize_data(data_reshaped)

        self.assertLessEqual(data_normalized.all(), 1)
        self.assertGreaterEqual(data_normalized.all(), 0)

        data_inverse_transformed = model._LSTMModel__inverse_transform(data_normalized)
        data_inverse_transformed = data_inverse_transformed.reshape(1, -1)

        for i in range(0, len(data)):
            self.assertAlmostEqual(data[i], data_inverse_transformed[0][i], delta=0.005)

    def test_extract_prediction_date_when_previous_date_is_weekday(self):
        ''' Test if the prediction date extraction is correct when the last price date is a weekday different than Friday '''
        model = LSTMModel('')
        prev_day_date = [None] * 3

        # Set year
        prev_day_date[0] = 2023
        # Set month
        prev_day_date[1] = 12
        # Set day
        prev_day_date[2] = 4

        prediction_day_date = model._LSTMModel__extract_prediction_date(prev_day_date)

        self.assertEqual(2023, prediction_day_date[0][0])
        self.assertEqual(12, prediction_day_date[0][1])
        self.assertEqual(5, prediction_day_date[0][2])


    def test_extract_prediction_date_when_previous_date_is_weekday(self):
        ''' Test if the prediction date extraction is correct when the last price date is Friday '''
        model = LSTMModel('')
        prev_day_date = [None] * 3

        # Set year
        prev_day_date[0] = 2023
        # Set month
        prev_day_date[1] = 12
        # Set day
        prev_day_date[2] = 8

        prediction_day_date = model._LSTMModel__extract_prediction_date(prev_day_date)

        self.assertEqual(2023, prediction_day_date[0][0])
        self.assertEqual(12, prediction_day_date[0][1])
        self.assertEqual(11, prediction_day_date[0][2])




    def prepare_test_data(self):
        data = np.empty(30)
        i = 0
        for x in data:
            x = random.randint(1, 20)
            data[i] = x
            i += 1
        return data

