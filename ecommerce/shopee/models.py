from django.db import models

# Create your models here.

class UserData(models.Model):
    name = models.CharField(max_length=255, unique=True)
    phone_no = models.PositiveIntegerField(unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    