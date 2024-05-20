from django.db import models
from book.models import Category, Product
# Create your models here.
class Mobile(models.Model):
    name = models.CharField(max_length = 255)
    price = models.FloatField()
    createAt = models.DateField(auto_now_add = True)
    description = models.CharField(max_length = 255, default = '')
    brand = models.CharField(max_length=100)
    specifications = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'mobile'
        app_label = 'mobile'
        verbose_name = "mobile"
        verbose_name_plural = "mobiles"

    def __str__(self):
        return self.name