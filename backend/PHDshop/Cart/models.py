from django.db import models
from good.models import *
from customer.models import *

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")  # Dùng OneToOneField để đảm bảo mỗi người dùng có một giỏ hàng duy nhất
    notes = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user}"


class CartGood(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_Goods', default=None)
    good = models.ForeignKey(Good, on_delete=models.CASCADE, related_name='cart_Goods')
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('cart', 'good') 




