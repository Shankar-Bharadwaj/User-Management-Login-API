from django.db import models

from location.models import Country
from features.models import AppFeatures

class CompanyDetail(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_code = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    company_logo_path = models.CharField(max_length=255)
    company_business_id = models.IntegerField()
    company_revenue_id = models.IntegerField()
    company_website = models.URLField()
    company_gstin = models.CharField(max_length=255)
    company_status = models.CharField(max_length=1)
    feedback_flag = models.CharField(max_length=1)
    company_dawn = models.TimeField()
    company_dusk = models.TimeField()
    company_timeslice = models.TimeField()
    bank_name = models.CharField(max_length=255)
    bank_code = models.CharField(max_length=255)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    merchant_id = models.TextField()
    merchant_secret_key = models.TextField()
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    radius = models.CharField(max_length=255)
    customer_app = models.CharField(max_length=1)
    appointment_auto_confirm = models.BooleanField()
    FSSAI = models.CharField(max_length=255)


class CompanyFeatures(models.Model):
    feature_id = models.ForeignKey(AppFeatures, on_delete=models.CASCADE)
    company_id = models.ForeignKey(CompanyDetail, on_delete=models.CASCADE)
    company_feature_status = models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')])
