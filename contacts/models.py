from django.db import models

# Create your models here.
class ContactDetail(models.Model):
    contact_id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=255)
    email = models.EmailField()
    pincode = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
