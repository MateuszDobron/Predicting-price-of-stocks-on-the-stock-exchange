# Author: Piotr Cieślak

from django.db import models
from django.contrib.auth.models import User

''' This class is a representation of the "Address" table in the database '''
class Address(models.Model):
    city = models.CharField(max_length=1)
    street = models.CharField(max_length=90)
    postal_code = models.CharField(max_length=20)


''' This class is a representation of the "Profile" table in the database '''
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=9)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, primary_key=True)


''' This class is a representation of the "Company" table in the database '''
class Company(models.Model):
    company = models.CharField(max_length=20)
    ticker = models.CharField(max_length=5)
