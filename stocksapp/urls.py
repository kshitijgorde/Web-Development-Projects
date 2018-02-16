from django.conf.urls import url
from stocksapp import views
app_name = 'stocksapp'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name = 'home'),
    url(r'^upload/', views.FileUploadView.as_view(), name='upload_csv'),
    url(r'^company_tickers/', views.company_tickers_view, name='company_tickers'),
    url(r'^company_overview/(?P<pk>\d+)/', views.company_overview, name='company_overview'),
    url(r'^live_ticker_pricing/', views.live_ticker_price, name='live_ticker_price'),
    url(r'^purge_database/', views.purge_database, name='purge_database'),
    url(r'^stock_comparison/', views.stock_comparison, name='stock_comparison'),
    url(r'^get_json/(?P<pk>\d+)', views.get_stock_data, name='stock_data'),
    url(r'^test/', views.TestView.as_view(), name='json'),
    url(r'^portfolio/', views.PortfolioList.as_view(), name='portfolio_list'),
    url(r'^test_portfolio_insert/', views.test_portfolio_insert, name='portfolio_insert'),
    url(r'^create_portfolio/', views.CreatePortfolio, name='create_portfolio'),
    url(r'^check_portfolio_name/(?P<portfolio_name>\w+)', views.check_portfolio_name, name='check_portfolio_name'),
    url(r'^portfolio_performance/(?P<pk>\w+)', views.portfolio_performance, name='portfolio_performance'),
    url(r'^portfolio_performance_page/(?P<pk>\w+)', views.portfolio_performance_page, name='portfolio_performance_page'),
    url(r'^company_comparison_endpoint/', views.company_comparison_service, name='company_comparison_service'),

]