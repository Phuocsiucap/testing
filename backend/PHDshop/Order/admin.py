from django.contrib import admin
from .models import *

# Registering Admin model
admin.site.register(Order)
admin.site.register(Payment)

admin.site.register(OrderGood)
