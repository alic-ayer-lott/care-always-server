from django.db import models
from django.contrib.auth.models import User

class UserCondition(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    condition = models.ForeignKey("Condition", on_delete=models.CASCADE)