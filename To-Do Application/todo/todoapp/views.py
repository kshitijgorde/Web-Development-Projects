from django.shortcuts import render
from django.http import HttpResponse
from .models import Task
from django.views.generic import TemplateView, DetailView, ListView
# Create your views here.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin


from django.contrib.auth import get_user_model
User = get_user_model()

class IndexView(ListView):
    model = Task
    template_name = 'todoapp/index.html'

    




class DetailedTaskView(DetailView):
    model = Task

