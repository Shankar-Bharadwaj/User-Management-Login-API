from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class UserManagement(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user_mobile = models.BigIntegerField()
    international_calling_code = models.IntegerField()
    calling_country = models.CharField(max_length=5)
    email = models.EmailField(unique=True)
    user_pin = models.CharField(max_length=255)
    fcm_key = models.TextField(null=True, blank=True)
    isPinResetRequested = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_mobile', 'international_calling_code', 'calling_country', 'user_pin', 'isPinResetRequested']


    def __str__(self):              
        return self.email
    
    def natural_key(self):
        return (self.email,)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
