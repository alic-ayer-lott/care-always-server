from django.db import models
from django.contrib.auth.models import User

class UserProvider(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.ForeignKey("Provider", on_delete=models.CASCADE)