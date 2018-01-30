from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        fields = ('task_name', 'task_priority')
        model = Task
