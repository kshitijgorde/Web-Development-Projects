from django.shortcuts import render
from django.http import HttpResponse
from .models import Task
from django.views.generic import TemplateView, DetailView, ListView
# Create your views here.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin
from django.contrib.auth.mixins import LoginRequiredMixin


from django.contrib.auth import get_user_model
User = get_user_model()

class IndexView(ListView):
    model = Task
    template_name = 'todoapp/index.html'
    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Task.objects.filter(user = self.request.user)
        else:
            return None

class DetailedTaskView(DetailView):
    model = Task



class CreateTask(LoginRequiredMixin, generic.CreateView):
    form_class = forms.TaskForm
    success_url = reverse_lazy("todoapp:index")
    template_name = "todoapp/task_form.html"
    # fields = ('task_name', 'task_priority')
    # model = Task
    #
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeleteTask(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("todoapp:index")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Task Deleted")
        return super().delete(*args, **kwargs)















