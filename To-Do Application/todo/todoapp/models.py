from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.

User = get_user_model()

class Task(models.Model):
    user = models.ForeignKey(User, related_name = 'task')
    task_name = models.CharField(max_length = 256)
    task_priority = models.CharField(max_length = 10)

    def __str__(self):
        return self.task_name

