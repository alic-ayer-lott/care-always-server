from django.db import models

class Question(models.Model):
    
    content = models.TextField()
    appointment = models.ForeignKey("Appointment", on_delete=models.DO_NOTHING)