from django.db import models
from datetime import datetime


class Brand(models.Model):
    brandName = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class Category(models.Model):
    categoryName = models.CharField(max_length=255)


class Sale(models.Model):
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def is_active(self):
        now = datetime.now()
        return self.start_date <= now <= self.end_date


class Good(models.Model):
    id = models.AutoField(primary_key=True)
    goodName = models.CharField(max_length=255)
    specifications = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    amount = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    # sales = models.ManyToManyField(Sale, related_name='goods', blank=True)

    # @property
    # def discounted_price(self):
    #     """
    #     Tính giá giảm giá dựa trên chương trình khuyến mãi đang hoạt động.
    #     Nếu không có khuyến mãi, trả về giá gốc.
    #     """
    #     active_sales = [sale for sale in self.sales.all() if sale.is_active()]
    #     if active_sales:
    #         max_discount = max(sale.discount_percentage for sale in active_sales)
    #         return self.price * (1 - max_discount / 100)
    #     return self.price
