from django.db import models
from authentication.models import UserManagement
from products.models import Product

# Create your models here.
class Merchant(models.Model):
    merchant_id = models.OneToOneField(UserManagement, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    products = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    def __str__(self):              
        return self.name
