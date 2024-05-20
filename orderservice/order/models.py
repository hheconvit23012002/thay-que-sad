from django.db import models
from django.utils.translation import gettext_lazy as _

class Order(models.Model):
    userId = models.IntegerField()
    customer_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    order_date = models.DateField(auto_now_add=True)
    status_pay = models.IntegerField(default=0)

    def __str__(self):
        return f"Order of {self.customer_name}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_id = models.IntegerField(null=True)
    quantity = models.PositiveIntegerField(default=1)
    price  = models.FloatField(null=False)
    images = models.TextField(null=True)
    product_name = models.CharField(max_length=255,null=True)
    
    def __str__(self):
        return f"{self.name} in order of {self.fullname}"