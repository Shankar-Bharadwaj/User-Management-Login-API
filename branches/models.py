from django.db import models
from contacts.models import ContactDetail
from companies.models import CompanyDetail


class BranchDetail(models.Model):
    branch_id = models.AutoField(primary_key=True)
    company_id = models.ForeignKey(CompanyDetail, on_delete=models.CASCADE)
    branch_status = models.CharField(max_length=1)
    contact_id = models.ForeignKey(ContactDetail, on_delete=models.CASCADE)
    branch_type = models.CharField(max_length=1)
    work_type = models.IntegerField()
    cash_drawer = models.CharField(max_length=1, choices=[('M', 'Main'), ('S', 'Sub')])
    zone_id = models.IntegerField()
