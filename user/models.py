from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

import re


# Create your models here.


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    dob = models.DateField()
    address = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=5)
    country = models.CharField(
        max_length=50
    )

    def __str__(self):
        return f'{self.user}'

    def clean(self):
        error_messages = {}
        if re.search(r'[^0-6]', self.zipcode) or len(self.zipcode) < 5:
            error_messages['zipcode'] = 'Invalid Zipcode'
        if error_messages:
            raise ValidationError(error_messages)
