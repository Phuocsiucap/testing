from django.contrib import admin
from .models import Voucher, VoucherUser

# Register your models here.
admin.site.register(Voucher)
admin.site.register(VoucherUser)
