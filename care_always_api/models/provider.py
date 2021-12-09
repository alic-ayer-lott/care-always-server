from django.db import models
from django.contrib.auth.models import User

class Provider(models.Model):
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialty = models.CharField(max_length=50)
    practice = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    patients = models.ManyToManyField(User, through="UserProvider", related_name="providers")



