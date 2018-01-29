from django.shortcuts import render
from User_App.models import User
from . import forms
# Create your views here.

def index(request):
    my_index_dict = {'index_content':"Welcome to User's Info. Type /users to view list of Users!"}
    return render(request, 'User_MTV/index.html', context = my_index_dict)

def users_info(request):
    users = User.objects.all()
    my_users = {'users_info':users}
    return render(request, 'User_MTV/user_info.html', context = my_users)

def form_name_view(request):
    form = forms.FormName()

    if request.method == 'POST':
        form = forms.FormName(request.POST)
        if form.is_valid():
            print('Validation Success!')
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            text = form.cleaned_data['text']
            print(name)
            print(email)
            print(text)

    return render(request, 'User_MTV/form_page.html', {'form':form})
