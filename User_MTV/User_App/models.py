from django.db import models

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 264, unique = True)

    def __str__(self):
        return first_name + last_name
