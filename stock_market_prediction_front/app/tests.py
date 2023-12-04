# Author: Piotr Cieślak
import numpy
from django.test import TestCase
from django.contrib import auth
from django.core.exceptions import ValidationError
import yfinance as yf
from .models import Profile
from.application.file_validator import FileValidator
import random
import numpy as np
from lstm_model.lstm_model import LSTMModel
from unittest.mock import patch

class UserRegisterCase(TestCase):
    # def setUp(self):
    #     self.email = 'test_email@email.com'


    def test_user_register_correctly(self):
        ''' Test if when user provides correct data, he gets registered successfully '''

        # Given register credentials are correct
        email = 'test_email@gmail.com'
        password = 'Test!123'
        confirm_password = 'Test!123'
        phone_number = '123123123'
        city = 'Warsaw'
        street = 'Warszawska 12'
        postal_code = '12-123'

        # When user tries to register
        response = self.register_user(email, password, confirm_password, phone_number, city, street, postal_code)

        # Then user registers successfully and is authenticated on the website
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response=response, expected_url='/home/')

        user = auth.get_user(self.client)

        assert user.is_authenticated


    def test_user_register_email_validation_error(self):
        ''' Test if when user provides wrong register data, he does not get registered and an appropriate error is shown '''

        # Given register email is incorrect
        email = 'test_email'
        password = 'Test!123'
        confirm_password = 'Test!123'
        phone_number = '123123123'
        city = 'Warsaw'
        street = 'Warszawska 12'
        postal_code = '12-123'

        # When user tries to register
        response = self.register_user(email, password, confirm_password, phone_number, city, street, postal_code)

        self.assertEqual(response.status_code, 400)
        self.assertRaises(expected_exception=ValidationError)
        self.assertRaisesMessage(expected_exception=ValidationError, expected_message='Email must be valid!')

    def test_user_register_password_validation_error(self):
        ''' Test if when user provides wrong register data, he does not get registered and an appropriate error is shown '''

        # Given register password is incorrect
        email = 'test_email@email.com'
        password = 'Test!123'
        confirm_password = 'Test!123456'
        phone_number = '123123123'
        city = 'Warsaw'
        street = 'Warszawska 12'
        postal_code = '12-123'

        # When user tries to register
        response = self.register_user(email, password, confirm_password, phone_number, city, street, postal_code)

        self.assertEqual(response.status_code, 400)
        self.assertRaises(expected_exception=ValidationError)
        self.assertRaisesMessage(expected_exception=ValidationError, expected_message='Passwords do not match')

    def test_user_register_phone_validation_error(self):
        ''' Test if when user provides wrong register data, he does not get registered and an appropriate error is shown '''

        # Given register password is incorrect
        email = 'test_email@email.com'
        password = 'Test!123'
        confirm_password = 'Test!123'
        phone_number = 'abc123123'
        city = 'Warsaw'
        street = 'Warszawska 12'
        postal_code = '12-123'

        # When user tries to register
        response = self.register_user(email, password, confirm_password, phone_number, city, street, postal_code)

        self.assertEqual(response.status_code, 400)
        self.assertRaises(expected_exception=ValidationError)
        self.assertRaisesMessage(expected_exception=ValidationError,
                                 expected_message='Phone number must contain only numbers')

    def test_user_register_postal_code_validation_error(self):
        ''' Test if when user provides wrong register data, he does not get registered and an appropriate error is shown '''

        # Given register password is incorrect
        email = 'test_email@email.com'
        password = 'Test!123'
        confirm_password = 'Test!123'
        phone_number = '123123123'
        city = 'Warsaw'
        street = 'Warszawska 12'
        postal_code = '123-123'

        # When user tries to register
        response = self.register_user(email, password, confirm_password, phone_number, city, street, postal_code)

        self.assertEqual(response.status_code, 400)
        self.assertRaises(expected_exception=ValidationError)
        self.assertRaisesMessage(expected_exception=ValidationError, expected_message='Postal code must be valid!')

    def test_user_register_same_email(self):
        ''' Test if when user provides wrong register data, he does not get registered and an appropriate error is shown '''

        email = 'test_email2@gmail.com'
        password = 'Test!123'
        confirm_password = 'Test!123'
        phone_number = '123123123'
        city = 'Warsaw'
        street = 'Warszawska 12'
        postal_code = '12-123'

        response = self.register_user(email, password, confirm_password, phone_number, city, street, postal_code)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response=response, expected_url='/home/')

        response = self.register_user(email, password, confirm_password, phone_number, city, street, postal_code)

        self.assertEqual(response.status_code, 400)
        self.assertRaises(expected_exception=ValidationError)
        self.assertRaisesMessage(expected_exception=ValidationError,
                                 expected_message='User with such email already exists!')

    def register_user(self, email, password, confirm_password, phone_number, city, street, postal_code):
        return self.client.post(path='/register/', data={
            'email': email,
            'password': password,
            'confirm_password': confirm_password,
            'phone_number': phone_number,
            'city': city,
            'street': street,
            'postal_code': postal_code
        })


class UserLoginCase(TestCase):

    def test_user_login_correctly(self):
        ''' Test if when user provides correct credentials, he gets logged in successfuly '''

        # Given
        email = 'test_email3@gmail.com'
        password = 'Test!123'

        self.create_dummy_user(email, password)

        response = self.client.post(path='/login/', data={
            'email': email,
            'password': password
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response=response, expected_url='/home/')

    def test_user_login_wrong_credentials(self):
        ''' Test if when user provides wrong credentials, he does not get logged in '''

        email = 'non_existing_user_mail@mail.com'
        password = 'Test!123'

        response = self.client.post(path='/login/', data={
            'email': email,
            'password': password
        })

        self.assertEqual(response.status_code, 403)

        user = auth.authenticate(username=email, email=email, password=password)

        assert user is None

    def create_dummy_user(self, email, password):
        email = email
        password = password
        confirm_password = password
        phone_number = '123123123'
        city = 'Warsaw'
        street = 'Warszawska 12'
        postal_code = '12-123'

        self.register_user(email, password, confirm_password, phone_number, city, street, postal_code)

    def register_user(self, email, password, confirm_password, phone_number, city, street, postal_code):
        return self.client.post(path='/register/', data={
            'email': email,
            'password': password,
            'confirm_password': confirm_password,
            'phone_number': phone_number,
            'city': city,
            'street': street,
            'postal_code': postal_code
        })

class YahooFinApiConnectionCase(TestCase):
    ''' Test connection with yahoo finance API '''

    def test_yahoo_finance_api_connection(self):
        exception_raised = False
        ticker = yf.Ticker('AAPL')
        try:
            ticker.basic_info
        except:
            exception_raised = True

        self.assertEqual(exception_raised, False)

class LstmModelCase(TestCase):

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

class ProfileEditCase(TestCase):
    def test_edit_profile_information(self):
        email = 'dummy_user@mail.com'
        password = 'Test!123'
        self.create_dummy_user(email, password)

        user = auth.get_user(self.client)
        profile = Profile.objects.get(user__email=email)

        self.assertIsNotNone(profile)
        self.assertEqual(profile.phone_number, '123123123')

        new_phone_number = '123456789'
        city = profile.address.city
        street = profile.address.street
        postal_code = profile.address.postal_code

        response = self.client.post('/profile/', data={
            'phone_number': new_phone_number,
            'city': city,
            'street': street,
            'postal_code': postal_code
        })

        self.assertEqual(response.status_code, 200)

        profile = Profile.objects.get(user__email=email)

        self.assertEqual(profile.phone_number, new_phone_number)


    def test_profile_not_edited_because_wrong_information(self):
        email = 'dummy_user@mail.com'
        password = 'Test!123'
        self.create_dummy_user(email, password)

        user = auth.get_user(self.client)
        profile = Profile.objects.get(user__email=email)

        self.assertIsNotNone(profile)
        self.assertEqual(profile.phone_number, '123123123')

        phone_number = profile.phone_number
        city = profile.address.city
        street = profile.address.street
        new_postal_code = '123-12'

        response = self.client.post('/profile/', data={
            'phone_number': phone_number,
            'city': city,
            'street': street,
            'postal_code': new_postal_code
        })

        self.assertEqual(response.status_code, 200)

        profile = Profile.objects.get(user__email=email)

        self.assertEqual(profile.address.postal_code, '12-123')
        self.assertRaisesMessage(expected_exception=ValidationError, expected_message='Postal code must be valid!')


    def create_dummy_user(self, email, password):
        email = email
        password = password
        confirm_password = password
        phone_number = '123123123'
        city = 'Warsaw'
        street = 'Warszawska 12'
        postal_code = '12-123'

        self.register_user(email, password, confirm_password, phone_number, city, street, postal_code)

    def register_user(self, email, password, confirm_password, phone_number, city, street, postal_code):
        return self.client.post(path='/register/', data={
            'email': email,
            'password': password,
            'confirm_password': confirm_password,
            'phone_number': phone_number,
            'city': city,
            'street': street,
            'postal_code': postal_code
        })




# class ModelTestFileCase(TestCase):
#     def test_invalid_test_file_because_wrong_extension(self):
