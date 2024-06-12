from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class ExtendUser(AbstractUser):
    email = models.EmailField(blank=False, max_length=255, verbose_name="Email")
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    