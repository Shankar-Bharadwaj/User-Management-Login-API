from django.db import models

# Create your models here.
class AppFeatures(models.Model):
    feature_id = models.AutoField(primary_key=True)
    feature_name = models.CharField(max_length=255)
    feature_type = models.CharField(max_length=1)
    feature_description = models.TextField()
    feature_status = models.CharField(max_length=1)
