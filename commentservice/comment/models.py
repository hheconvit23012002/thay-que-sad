from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Comment(models.Model):
    comment = models.CharField(max_length = 255)
    rate = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    userId = models.IntegerField(null=True)
    productId = models.IntegerField(null=True)
    createAt = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.comment