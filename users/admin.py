from django.contrib import admin
from .models import UserDetail, UserCompanies, UserBranchDetail

# Register your models here.
admin.site.register(UserDetail)
admin.site.register(UserCompanies)
admin.site.register(UserBranchDetail)
