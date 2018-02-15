from django.conf.urls import url
from stocksapp import views
app_name = 'stocksapp'

urlpatterns = [
    url(r'^/', views.IndexView.as_view(), name = 'home'),
    url(r'^upload/', views.FileUploadView.as_view(), name='upload_csv'),
    url(r'^company_tickers/', views.company_tickers_view, name='company_tickers'),
    url(r'^company_overview/(?P<pk>\d+)/', views.company_overview, name='company_overview'),
    url(r'^build_portfolio/', views.FileUploadView.as_view(), name='build_portfolio'),
    url(r'^live_data/', views.FileUploadView.as_view(), name='live_data'),
    url(r'^purge_database/', views.purge_database, name='purge_database'),
    url(r'^stock_comparison/', views.FileUploadView.as_view(), name='stock_comparison'),
]