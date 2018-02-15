from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import pandas as pd
import os
from django.conf import settings
from stocksapp.models import Company, StockData
from django.views.generic.edit import FormView
from datetime import datetime
from .forms import UploadCSVForm
from django.views.generic import TemplateView, DetailView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.

class IndexView(TemplateView):
    template_name = 'stocksapp/index.html'


class FileUploadView(FormView, SuccessMessageMixin):
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
    company_objects = Company.objects.all()
    return render(request, 'stocksapp/company_details.html', {'company_objects':company_objects})


def company_overview(request,pk):
    company = Company.objects.filter(pk=pk)[0]
    data = {'name':company.company_name}
    return JsonResponse(data)

def purge_database(request):
    Company.objects.all().delete()
    StockData.objects.all().delete()
    return HttpResponse('Deleted Successfully!')





