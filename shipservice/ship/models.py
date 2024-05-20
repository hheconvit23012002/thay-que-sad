from django.db import models

# Create your models here.

class Ship(models.Model):
    shiperId = models.IntegerField(null=True)
    orderId =models.IntegerField(null=True)
    address = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null= True)
    created_at = models.DateTimeField(auto_now_add=True)
    des = models.TextField(null=True)
    status = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.address
    
class ShipDetail(models.Model):
    ship = models.ForeignKey(Ship,related_name='details', on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address