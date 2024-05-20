from django.db import models

# Create your models here.
class Cart(models.Model):
    userId = models.IntegerField()
    updateAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.userId}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product_id = models.IntegerField(null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.id} in cart of {self.cart.id}"