from django.db import models

# Create your models here.
class Currency(models.Model):
    currency_id = models.AutoField(primary_key=True)
    currency_name = models.CharField(max_length=255)
    currency_code = models.CharField(max_length=5)
    country_code = models.CharField(max_length=5)
