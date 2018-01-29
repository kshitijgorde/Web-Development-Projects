from django.conf.urls import url
from User_App import views


urlpatterns = [
    url(r'^$',views.users_info, name = 'users_info'),
    url(r'^form/',views.form_name_view, name = 'form_name_view'),
]
