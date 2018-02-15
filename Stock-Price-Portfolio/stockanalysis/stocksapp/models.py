from django.db import models

# Create your models here.
class Company(models.Model):
    id = models.AutoField(primary_key = True)
    ticker = models.CharField(max_length=20)
    company_name = models.CharField(max_length=200)
    description = models.TextField()
    gics_sector = models.CharField(max_length=200)
    gics_industry = models.CharField(max_length=200)
    gics_industry_group = models.CharField(max_length=200)
    gics_sub_industry_group = models.CharField(max_length=200)


    def __str__(self):
        return str(self.id)

class StockData(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()
    closing_price = models.FloatField()
    volume = models.BigIntegerField()

    def __str__(self):
        return 'Stocks-<company'+str(self.company_id)+'>-'+str(self.date)



