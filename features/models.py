from django.db import models


class AppFeatures(models.Model):
    feature_id = models.AutoField(primary_key=True)
    feature_name = models.CharField(max_length=255)
    feature_type = models.CharField(max_length=10)
    feature_description = models.TextField()
    feature_status = models.BooleanField()

    def __str__(self):
        return self.feature_name
