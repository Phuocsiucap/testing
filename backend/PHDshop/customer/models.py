from django.db import models

class User(models.Model):
    fullName = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    userType = models.CharField(max_length=50, default="Silver User", blank=True)
    loyaltyPoints = models.IntegerField(default=0, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.fullName


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=255, null=True)
    addressct = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)  # Địa chỉ mặc định

    def __str__(self):
        return f"{self.phone} - {self.addressct} -{self.city} - {self.is_default}"