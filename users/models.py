from django.db import models
from companies.models import CompanyDetail
from branches.models import BranchDetail


class UserDetail(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_dob = models.DateField()
    marital_status = models.BooleanField(default=False)
    user_gender = models.BooleanField(default=False)
    user_status = models.BooleanField(default=False)

    def __str__(self):              
        return self.first_name


class UserCompanies(models.Model):
    user_id = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    company_id = models.ForeignKey(CompanyDetail, on_delete=models.CASCADE)
    user_type = models.BooleanField(default=False)
    status = models.BooleanField(default=False)


class UserBranchDetail(models.Model):
    user_id = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    branch_id = models.ForeignKey(BranchDetail, on_delete=models.CASCADE)
    user_branch_status = models.BooleanField(default=False)
