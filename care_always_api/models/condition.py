from django.db import models

class Condition(models.Model):

    diagnosis = models.CharField(max_length=100)