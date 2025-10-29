from rest_framework import serializers
from .models import Order, OrderGood
from Voucher.models import Voucher
from good.models import Good
from Voucher.models import Voucher
from customer.models import User
from django.contrib.auth.models import User as Admin
from vnpay_python.models import Payment

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset =User.objects.all())
    admin = serializers.PrimaryKeyRelatedField(queryset =Admin.objects.all())
    voucher = serializers.PrimaryKeyRelatedField(queryset=Voucher.objects.all(), required=False)  
    pay = serializers.PrimaryKeyRelatedField(queryset=Payment.objects.all(), write_only= True)
    class Meta:
        model = Order
        fields = '__all__'
class OrderGoodSerializer(serializers.ModelSerializer):
    good = serializers.PrimaryKeyRelatedField(queryset =Good.objects.all() )
    class Meta:
        model = OrderGood
        fields = ['order', 'good', 'quantity']
