from django.db import models
from book.models import Category, Product
# Create your models here.

class Clothes(models.Model):
    name = models.CharField(max_length = 255)
    price = models.FloatField()
    createAt = models.DateField(auto_now_add = True)
    description = models.CharField(max_length = 255, default = '')
    brand = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'clothes'
        app_label = 'clothes'
        verbose_name = "clothes"
        verbose_name_plural = "clothes"

    def __str__(self):
        return self.name