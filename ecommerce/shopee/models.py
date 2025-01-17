from django.db import models
 

# Create your models here.

class UserData(models.Model):
    name = models.CharField(max_length=255, unique=True)
    phone_no = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    