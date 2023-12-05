# Author: Piotr Cieślak

from django import forms
import re
from django.core.exceptions import ValidationError


# todo
# implement countries?
class EditProfileForm(forms.Form):
    phone_number = forms.CharField(min_length=9, max_length=9)
    city = forms.CharField(max_length=40)
    street = forms.CharField(max_length=90)
    postal_code = forms.CharField(max_length=20)

    def set_fields(self, profile):
        ''' This function sets the initial fields of the form as the values of
        the fields present in the database for the currently logged-in user '''

        self.fields['phone_number'].initial = profile.phone_number
        self.fields['city'].initial = profile.address.city
        self.fields['street'].initial = profile.address.street
        self.fields['postal_code'].initial = profile.address.postal_code

    def clean(self):

        ''' This function is used for form validation and returns an appropriate error in case of invalid input '''

        super(EditProfileForm, self).clean()

        phone_number = self.cleaned_data.get('phone_number')
        city = self.cleaned_data.get('city')
        street = self.cleaned_data.get('street')
        postal_code = self.cleaned_data.get('postal_code')

        if any(c.isalpha() for c in phone_number):
            ''' Check if there is an non numerical character in the phone number '''

            self.__set_error('phone_number', 'Phone number must contain only numbers')

        if not re.fullmatch("\d{2}-\d{3}", postal_code):
            ''' Validate the postal code to be compliant with the polish standard {2 digits}-{3 digits} '''

            self.__set_error('postal_code', 'Postal code must be valid!')

        return self.cleaned_data

    def __set_error(self, field, error_message):
        ''' This function sets the error message and html class of invalid field '''

        self.errors[field] = self.error_class([error_message])
        self.fields[field].widget.attrs['class'] = 'error'
        raise ValidationError(error_message)