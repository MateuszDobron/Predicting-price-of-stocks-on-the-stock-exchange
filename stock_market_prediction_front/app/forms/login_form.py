# Author: Piotr Cieślak

from django import forms
from django.core.exceptions import ValidationError


# todo
# form validation
class LoginForm(forms.Form):
    ''' Form used for user login. User logs in with an email and password '''

    email = forms.CharField(max_length=60)
    password = forms.CharField(max_length=60, widget=forms.PasswordInput)

    def clean(self):

        super(LoginForm, self).clean()

    def set_wrong_credentials_error(self):
        ''' This function sets the html classes of labels to "error" in case of wrong credentials '''

        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        self.__set_error('email', 'Wrong credentials!')
        self.fields['email'].widget.attrs['class'] = 'error'

    def __set_error(self, field, error_message):
        ''' This function sets the error message and html class of invalid field '''

        self.errors[field] = self.error_class([error_message])
        self.fields[field].widget.attrs['class'] = 'error'

