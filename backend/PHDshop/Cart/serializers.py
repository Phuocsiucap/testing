from rest_framework import serializers
from .models import Cart, CartGood
from good.serializer import GoodSerializer
from good.models import Good
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'  

class CartGoodSerializer(serializers.ModelSerializer):
    # good= GoodSerializer()
    good = serializers.PrimaryKeyRelatedField(queryset=Good.objects.all())  # Chỉ cho phép gửi ID của sản phẩm
    class Meta:
        model = CartGood
        fields = '__all__'  
    def to_representation(self, instance):
        """
        Custom representation to include detailed Good information
        """
        representation = super().to_representation(instance)
        representation['good'] = GoodSerializer(instance.good).data  # Serialize thông tin sản phẩm đầy đủ khi trả về
        return representation