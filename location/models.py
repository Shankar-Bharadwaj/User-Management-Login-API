from django.db import models
from finance.models import Currency


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_code = models.CharField(max_length=5)
    country_name = models.CharField(max_length=255)
    mobile_format_id = models.IntegerField()
    currency_id = models.ForeignKey(Currency, on_delete=models.CASCADE)
