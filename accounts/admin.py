from django.contrib import admin
from stocksapp.models import StockData, Company, Portfolio, PortfolioCompanies
# Register your models here.

admin.site.register(StockData)
admin.site.register(Company)
admin.site.register(Portfolio)
admin.site.register(PortfolioCompanies)
