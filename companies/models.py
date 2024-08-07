from django.db import models
from location.models import Country
from features.models import AppFeatures
import uuid
from user_management.utils import validate_aadhar_number, validate_pan_number, validate_gst_number


class CompanyDetail(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_code = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    company_business_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    company_gstin = models.CharField(max_length=255, validators=[validate_gst_number],  unique=True)
    company_status = models.CharField(max_length=10)
    company_dawn = models.TimeField()
    company_dusk = models.TimeField()
    company_timeslice = models.TimeField()
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    FSSAI = models.CharField(max_length=255, unique=True)
    aadhar_number = models.CharField(max_length=14, validators=[validate_aadhar_number])
    pan = models.CharField(max_length=10, validators=[validate_pan_number])
    company_address = models.TextField()
    business_type = models.CharField(max_length=255)


    # company_revenue_id = models.IntegerField()
    # company_website = models.URLField()
    # feedback_flag = models.CharField(max_length=10)
    # bank_name = models.CharField(max_length=255)
    # bank_code = models.CharField(max_length=255)
    # merchant_id = models.TextField()
    # merchant_secret_key = models.TextField()
    # latitude = models.CharField(max_length=255)
    # longitude = models.CharField(max_length=255)
    # radius = models.CharField(max_length=255)
    # customer_app = models.CharField(max_length=10)
    # appointment_auto_confirm = models.BooleanField()

    def __str__(self):
        return self.company_name


class CompanyFeatures(models.Model):
    feature_id = models.ForeignKey(AppFeatures, on_delete=models.CASCADE)
    company_id = models.ForeignKey(CompanyDetail, on_delete=models.CASCADE)
    company_feature_status = models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')])

    def __str__(self):
        return f'{self.company_id.company_name}-{self.feature_id.feature_name}'
