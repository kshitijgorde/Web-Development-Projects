from django.shortcuts import render
from django.http import HttpResponse
from .models import Task
from django.views.generic import TemplateView, DetailView
# Create your views here.

class IndexView(TemplateView):
    task_list = Task.objects.all()
    template_name = 'todoapp/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['task_list'] = Task.objects.all()
        return context


class DetailedTaskView(DetailView):
    model = Task



def index(request):
    task_list = Task.objects.all()
    return HttpResponse(task_list)

def detail(request, task_id):
    return HttpResponse("This is for %s" % task_id)