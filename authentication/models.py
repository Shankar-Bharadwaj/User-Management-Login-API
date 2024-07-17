from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserLoginManager(BaseUserManager):
    def create_user(self, email, user_mobile, international_calling_code, calling_country, user_pin=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not user_pin:
            raise ValueError('The Password field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            user_mobile=user_mobile,
            international_calling_code=international_calling_code,
            calling_country=calling_country,
            **extra_fields
        )
        user.set_user_pin(user_pin)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, user_mobile, international_calling_code, calling_country, user_pin=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, user_mobile, international_calling_code, calling_country, user_pin, **extra_fields)
    

class UserLogin(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    user_mobile = models.BigIntegerField()
    international_calling_code = models.IntegerField()
    calling_country = models.CharField(max_length=5)
    email = models.EmailField(unique=True)
    user_pin = models.CharField(max_length=255)
    fcm_key = models.TextField(null=True, blank=True)
    isPinResetRequested = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['user_mobile', 'user_pin', 'international_calling_code', 'calling_country']

    objects = UserLoginManager() 

    def __str__(self):
        return self.email
    
    def set_user_pin(self, raw_pin):
        self.user_pin = make_password(raw_pin)

    def check_user_pin(self, raw_pin):
        return check_password(raw_pin, self.user_pin)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
