import uuid
from django.db import models
from django.contrib.auth.models import User

class Preference(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    preference = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.preference}"
