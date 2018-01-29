from django.shortcuts import render
from django.http import HttpResponse
from first_app.models import Webpage, Topic, AccessRecord
# Create your views here.

def index(request):
    web_pages = AccessRecord.objects.order_by('date')
    date_dictionary = {"access_records": web_pages}
    return render(request, "first_app/index.html", context=date_dictionary)

def help(request):
    my_dict = {"help_content": "If you need any Help just call 911. Godspeed!"}
    return render(request, "first_app/help.html", context=my_dict)
