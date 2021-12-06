from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):

    date = models.DateField()
    time = models.TimeField()
    provider = models.ForeignKey("Provider", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey("Question")
