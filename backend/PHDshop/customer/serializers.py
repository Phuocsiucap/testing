from rest_framework import serializers
from .models import User, Address


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','fullName', 'email', 'password', 'userType', 'loyaltyPoints']

    def create(self, validated_data):
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.password = validated_data['password']
        return super(UserSerializer, self).update(instance, validated_data)
    
class AddressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Chỉ đọc, không yêu cầu trong payload

    class Meta:
        model = Address
        fields = '__all__'

    # def to_representation(self, instance):
    #     """
    #     Tùy chỉnh phản hồi để bao gồm thông tin chi tiết của user.
    #     """
    #     representation = super().to_representation(instance)
    #     # representation['user'] = UserSerializer(instance.user).data  # Serialize thông tin chi tiết của user
    #     return representation
