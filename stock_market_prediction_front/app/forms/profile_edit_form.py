# Author: Piotr Cieślak

from django import forms
from .countries import CountryField

class EditProfileForm(forms.Form):
    phone_number = forms.CharField(min_length=9, max_length=9)
    country = CountryField()
    city = forms.CharField(max_length=40)
    street = forms.CharField(max_length=90)
    postal_code = forms.CharField(max_length=20)