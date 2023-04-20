from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

import re


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    date_of_birth = models.DateField()
    address = models.CharField(max_length=50)
    address2 = models.CharField(max_length=5)
    city = models.CharField(max_length=30)
    

    def __str__(self):
        return f'{self.usuario}'

    def clean(self):
        error_messages = {}

        if error_messages:
            raise ValidationError(error_messages)
