from django.db import models

# Create your models here.

class Task(models.Model):

    task_name = models.CharField(max_length = 256)
    task_priority = models.CharField(max_length = 10)

    def __str__(self):
        return self.task_name
