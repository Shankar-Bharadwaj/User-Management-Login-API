from django.db import models
from companies.models import CompanyDetail
from branches.models import BranchDetail
from authentication.models import UserLogin


class UserDetail(models.Model):
    user_id = models.OneToOneField(UserLogin, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_dob = models.DateField()
    marital_status = models.BooleanField(default=False)
    user_gender = models.BooleanField(default=False)
    user_status = models.BooleanField(default=False)

    def __str__(self):              
        return self.first_name


class UserCompanies(models.Model):
    user_id = models.ForeignKey(UserLogin, on_delete=models.CASCADE)
    company_id = models.ForeignKey(CompanyDetail, on_delete=models.CASCADE)
    user_type = models.BooleanField(default=False)
    status = models.BooleanField(default=False)

    def __str__(self):              
        return f'{self.user_id.email} - {self.company_id.company_name}'


class UserBranchDetail(models.Model):
    user_id = models.ForeignKey(UserLogin, on_delete=models.CASCADE)
    branch_id = models.ForeignKey(BranchDetail, on_delete=models.CASCADE)
    user_branch_status = models.BooleanField(default=False)

    def __str__(self):              
        return f'{self.user_id} - {self.branch_id}'
