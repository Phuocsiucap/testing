from rest_framework import serializers
from .models import Good

class GoodSerializer(serializers.ModelSerializer):
    # discounted_price = serializers.DecimalField(
    #     max_digits=10, decimal_places=2, read_only=True
    # )
    # image = serializers.ImageField(required=False)  # Xử lý trường ảnh

    class Meta:
        model = Good
        fields = [
            'id', 'goodName', 'specifications', 'image', 'amount', 'price',
            'category', 'brand',
        ]