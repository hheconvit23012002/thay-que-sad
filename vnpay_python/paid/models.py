from django.db import models

# Create your models here.

class Paid(models.Model):
    order_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=255)
    total = models.FloatField(default=0)