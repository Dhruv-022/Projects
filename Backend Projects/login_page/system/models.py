#Here is an error to be resolved

from django.db import models

class CustomUser(models.Model):
    # unique=True prevents any two users from registering the exact same username
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username