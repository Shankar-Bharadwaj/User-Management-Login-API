from django.db import models
from django.contrib.auth.models import AbstractUser
from authentication.models import UserManagement

# Create your models here.
class ExtendUser(models.Model):
    user_id = models.OneToOneField(UserManagement, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(blank=False, max_length=255, verbose_name="Email")
    username = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    def __str__(self):              
        return self.username
