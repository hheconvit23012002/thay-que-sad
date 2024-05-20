from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    description = models.TextField(max_length=1500, blank=True)
    images = models.ImageField(upload_to='photos/products')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    class Meta:
        db_table = 'product'
        verbose_name = 'product'
        verbose_name_plural = 'product'

    def __str__(self):
        return self.type

class Book(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=1500, blank=True)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'book'
        verbose_name = 'book'
        verbose_name_plural = 'book'

    def __str__(self):
        return self.name