from django.contrib import admin
from stocksapp.models import StockData, Company
# Register your models here.

admin.site.register(StockData)
admin.site.register(Company)