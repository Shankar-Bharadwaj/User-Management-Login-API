from django.db import models
from companies.models import CompanyDetail
from branches.models import BranchDetail
from authentication.models import UserManagement


class UserDetail(models.Model):
    user_id = models.OneToOneField(UserManagement, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_dob = models.DateField()
    marital_status = models.BooleanField()
    user_gender = models.BooleanField()
    user_status = models.BooleanField()

    def __str__(self):              
        return self.username


class UserCompanies(models.Model):
    user_id = models.OneToOneField(UserManagement, on_delete=models.CASCADE)
    company_id = models.ForeignKey(CompanyDetail, on_delete=models.CASCADE)
    user_type = models.IntegerField()
    status = models.IntegerField()


class UserBranchDetail(models.Model):
    user_id = models.OneToOneField(UserManagement, on_delete=models.CASCADE)
    branch_id = models.ForeignKey(BranchDetail, on_delete=models.CASCADE)
    user_branch_status = models.IntegerField()
