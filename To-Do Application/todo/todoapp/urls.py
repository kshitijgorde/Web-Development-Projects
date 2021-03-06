from django.conf.urls import url
from . import views


app_name = 'todoapp'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name = 'index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailedTaskView.as_view(), name='detail'),
    url(r'^new/$', views.CreateTask.as_view(), name='create'),
    url(r"delete/(?P<pk>\d+)/$",views.DeleteTask.as_view(),name="delete"),
]
