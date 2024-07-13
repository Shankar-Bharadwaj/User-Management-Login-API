from django.db import models


class Currency(models.Model):
    currency_id = models.AutoField(primary_key=True)
    currency_name = models.CharField(max_length=255)
    currency_code = models.CharField(max_length=5)
    country_code = models.CharField(max_length=5)

    def __str__(self):
        return self.currency_name