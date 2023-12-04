# Author: Piotr Cieślak
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


# todo
# form validation
class RegisterForm(forms.Form):
    email = forms.CharField(max_length=60)
    password = forms.CharField(max_length=60, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=60, widget=forms.PasswordInput)
    phone_number = forms.CharField(min_length=9, max_length=9)
    city = forms.CharField(max_length=60)
    street = forms.CharField(max_length=60)
    postal_code = forms.CharField(max_length=60)

    def clean(self):
        ''' This function is used for form validation and returns an appropriate error in case of invalid input '''

        super(RegisterForm, self).clean()

        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        phone_number = self.cleaned_data.get('phone_number')
        city = self.cleaned_data.get('city')
        street = self.cleaned_data.get('street')
        postal_code = self.cleaned_data.get('postal_code')

        if len(email) < 3:
            self.__set_error('email', 'Minimum 1 character required')

        elif '@' not in email:
            ''' Check if email contains an "@" symbol '''

            self.__set_error('email', 'Email must be valid!')

        try:
            ''' Check if a user with such email already exists. If yes, return validation error '''

            User.objects.get(email__exact=email)
            self.__set_error('email', 'User with such email already exists!')
        except User.DoesNotExist:
            pass

        if len(password) < 8:
            self.__set_error('password', 'Password must contain at least 8 characters')

        elif password != confirm_password:
            ''' Check if password and confirm password are the same '''

            self.__set_error('confirm_password', 'Passwords do not match')

        if any(c.isalpha() for c in phone_number):
            self.__set_error('phone_number', 'Phone number must contain only numbers')

        if not re.fullmatch("\d{2}-\d{3}", postal_code):
            self.__set_error('postal_code', 'Postal code must be valid!')


        return self.cleaned_data

    def __set_error(self, field, error_message):
        ''' This function sets the error message and html class of invalid field '''

        self.errors[field] = self.error_class([error_message])
        self.fields[field].widget.attrs['class'] = 'error'
        raise ValidationError(error_message)