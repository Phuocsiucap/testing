from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    # order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['created_at', 'order_id']
