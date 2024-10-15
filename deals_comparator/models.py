from django.db import models

# Create your models here.

class Components(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    price = models.CharField(max_length=15, blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    available = models.BooleanField(default=True)
    component_type = models.CharField(max_length=50)
    vendor = models.CharField(max_length=50)
    date_added = models.DateField(auto_now_add=True)


