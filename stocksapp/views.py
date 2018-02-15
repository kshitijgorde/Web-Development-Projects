from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import pandas as pd
import os
import json
from django.conf import settings
from stocksapp.models import Company, StockData, PortfolioCompanies, Portfolio
from django.views.generic.edit import FormView
from datetime import datetime
from .forms import UploadCSVForm
from django.views.generic import TemplateView, DetailView, DeleteView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
import numpy as np
from scipy import stats
# Create your views here.

class IndexView(TemplateView):
    ''' Class based view for Index page '''
    template_name = 'stocksapp/index.html'


class FileUploadView(FormView, SuccessMessageMixin):
    ''' Controller for uploading files'''
    form_class = UploadCSVForm
    template_name = 'stocksapp/upload_csv.html'
    success_url = '/'
    success_message = "File data uploaded to database successfully"
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        files = request.FILES.getlist('file')
        if form.is_valid():
            csv_type = form.cleaned_data['select_type']
            for f in files:
                self.process_file_into_database(f, csv_type)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def process_file_into_database(self, file, csv_type):
        ''' A method to iterate through each row in csv and fill in database '''
        if csv_type == 'Company Data' or csv_type == 'company data':
            df = pd.read_csv(file)
            for index, row in df.iterrows():
                company_record = Company(index+1,row['Ticker'],row['Name'],row['Description'],row['GICS Sector'],row['GICS industry']
                                        ,row['GICS Industry group'],row['GICS Sub Industry Group'])
                company_record.save()
        elif csv_type == 'Stocks Data' or csv_type == 'stocks data':
            df_stocks = pd.read_csv(file)

            # Go through each stock and save it appropriately
            # StockData.objects.all().delete()
            for index, row in df_stocks.iterrows():
                c_id = Company.objects.filter(ticker__icontains=str(file).split('.')[0])
                stock_record = StockData(company_id=c_id[0], date = datetime.strptime(row['Date'].strip(), "%m/%d/%Y").date(), closing_price=row['PX_LAST'],
                                        volume=row['PX_VOLUME'])
                stock_record.save()

def company_tickers_view(request):
    ''' Returns all tickers from the database '''
    company_objects = Company.objects.all() #Return all company objects for tickers
    return render(request, 'stocksapp/company_details.html', {'company_objects':company_objects})


def company_overview(request,pk):
    ''' Gets required attributs from the Databse and sends to the view'''
    company = Company.objects.filter(pk=pk)[0]  # Get company object
    # stocks = StockData.objects.filter(company_id=pk)
    # related_data = []
    # for stock_item in stocks:
    #     related_data.append([(str(stock_item.date).replace('-','/')), stock_item.closing_price, stock_item.volume])
    data = {'name':company.company_name, 'company_id':pk,'description':company.description,
            'gics_sector':company.gics_sector, 'gics_industry':company.gics_industry,
            'gics_industry_group':company.gics_industry_group,
            'gics_sub_industry_group':company.gics_sub_industry_group}
    return JsonResponse(data)

def purge_database(request):
    ''' Caution!: Deletes all items from the database. Only valid on POST request '''
    if request.method == 'POST':
        #Purge the database
        Portfolio.objects.all().delete()
        PortfolioCompanies.objects.all().delete()
        Company.objects.all().delete()
        StockData.objects.all().delete()
        return HttpResponse('Deleted Successfully!')

    return HttpResponse('error')

class TestView(TemplateView):
    template_name = 'stocksapp/line_chart.html'

def get_stock_data(request, pk):
    ''' Returns json object for all stocks for a given company'''
    stocks = StockData.objects.filter(company_id=pk)
    data = []
    for stock_item in stocks:
        data.append([(str(stock_item.date).replace('-','/')), stock_item.closing_price, stock_item.volume])

    return HttpResponse(json.dumps(data))


class PortfolioList(ListView, LoginRequiredMixin):
    ''' Controller to view all available portfolios specific to the user'''
    model = Portfolio
    template_name = 'stocksapp/portfolio_list.html'
    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Portfolio.objects.filter(user = self.request.user)   #Get portfolio for current user
        else:
            return None


def test_portfolio_insert(request):
    '''test method'''
    data = {}
    name = ''
    if request.method == 'POST':
        data = request.POST.get('custom_portfolio') #Get values from ID in HTML
        name = request.POST.get('portfolioName')
    InsertPortfolioService(json.loads(data), request.user,name)
    return redirect('../portfolio')


def InsertPortfolioService(portfolio_dictionary, user_obj, name):
    ''' Inserting portfolio configuration onto the database '''
    portfolio_object = Portfolio(user=user_obj, portfolio_name=name)
    portfolio_object.save()
    for ticker, weight in portfolio_dictionary.items():
        # Get company id for the given ticker
        company_object = Company.objects.filter(ticker__icontains=ticker)[0]
        # now save details to portfolio PortfolioCompanies
        portfolio_companies = PortfolioCompanies(portfolio_id=portfolio_object,company_id=company_object,percentage=weight)
        portfolio_companies.save()

def CreatePortfolio(request):
    ''' Redirect to Create Portfolio page with ticker values '''
    template_name = 'stocksapp/create_portfolio.html'
    tickers = list(Company.objects.values_list('ticker',flat=True))
    result = ','.join(tickers)
    return render(request, template_name, {'tickers_list':result})


def check_portfolio_name(request, portfolio_name):
    return HttpResponse(len(list(Portfolio.objects.filter(user=request.user, portfolio_name__iexact=portfolio_name))) == 0)

def portfolio_performance(request, pk):
    ''' Calculates the performance of the portfolio over a date range'''
    portfolio_data = PortfolioCompanies.objects.filter(portfolio_id=pk)
    percentage_data = []    #get weights for every company in portfolio
    percentage_ticker = [] #Get tickers for all companies in the portfolio
    for percentage in portfolio_data:
        #Get ticker
        percentage_ticker.append(Company.objects.filter(id=percentage.company_id.id).values_list('ticker', flat=True)[0])
        percentage_data.append(percentage.percentage)


    portfolio_split = {}
    for x, y in zip(percentage_ticker, percentage_data):
        portfolio_split[x] = y


    stocks_data = []
    stocks_dates = StockData.objects.filter(company_id = portfolio_data[0].company_id, date__gte=datetime.strptime("2016-12-31", "%Y-%m-%d").date()).order_by('date').values_list('date', flat=True)
    final_data = []
    for item in portfolio_data:
        stocks_for_company = StockData.objects.filter(company_id = item.company_id, date__gte=datetime.strptime("2016-12-31", "%Y-%m-%d").date()).order_by('date').values_list('closing_price', flat=True)
        stocks_for_company = list(stocks_for_company)
        first_day_price = stocks_for_company[0]
        #Calculate percentage change
        stocks_percentage_change = np.around(((np.array(stocks_for_company) - first_day_price)/first_day_price)* 100,decimals=2)
        stocks_percentage_change *= item.percentage/100
        stocks_data.append(stocks_percentage_change)
    my_array = np.zeros(len(stocks_data[0]))
    for x in stocks_data:
        my_array += np.array(x)

    performance_overtime = np.around(my_array, decimals=2).tolist()

    for date, povertime in zip(stocks_dates, performance_overtime):
        final_data.append([str(date).replace('-','/'), povertime])

    finalized_data = {}
    finalized_data['PerformanceOvertime'] = final_data
    finalized_data['Splits'] = portfolio_split

    return HttpResponse(json.dumps(finalized_data))


def portfolio_performance_page(request, pk):
    return render(request, 'stocksapp/portfolio_performance.html', {'portfolioID':pk})

def stock_comparison(request):
    return render(request, 'stocksapp/stock_comparisons.html', {'company_objects':Company.objects.all()})

def company_comparison_service(request):
    ''' Compares the closing prices of 2 companies over a specific date range and Calculates regression '''
    companyA_id = request.GET.get('companyA')
    companyB_id = request.GET.get('companyB')
    tickerA = list(Company.objects.filter(id=companyA_id).values_list('ticker',flat=True))[0]
    tickerB = list(Company.objects.filter(id=companyB_id).values_list('ticker',flat=True))[0]
    date_range = [str(x).replace('-','/') for x in list(StockData.objects.values_list('date', flat=True).distinct())]
    closing_price_companyA = list(StockData.objects.filter(company_id = companyA_id).values_list('closing_price', flat=True))
    closing_price_companyB = list(StockData.objects.filter(company_id = companyB_id).values_list('closing_price', flat=True))
    dataPoints = []
    for x,y in zip(closing_price_companyA, closing_price_companyB):
        dataPoints.append([x,y])

    #Calculate LinearRegression
    slope, intercept, r_value, p_value, std_err = stats.linregress(closing_price_companyA, closing_price_companyB)
    fitted_line = []
    for x in closing_price_companyA:
        fitted_line.append([x, intercept + slope*x])
    #Pass data to the frontend
    #'corr':np.corrcoef(np.array(closing_price_companyA),np.array(closing_price_companyB))
    data = {'dataPoints':dataPoints,'date_range':date_range,'fitted_line':fitted_line,'tickerA':tickerA,'tickerB':tickerB}
    return HttpResponse(json.dumps(data))

def live_ticker_price(request):
    ''' Support for live ticker pricing'''
    return render(request, 'stocksapp/live_stock_price.html', {'company_objects':Company.objects.all()})


####





