from rest_framework import serializers
from .models import Voucher, VoucherUser,User
from customer.serializers import UserSerializer  # Import serializer của User nếu có

class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = '__all__'

class VoucherUserSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Chỉ cho phép gửi ID người dùng
    voucher = serializers.PrimaryKeyRelatedField(queryset=Voucher.objects.all(), write_only=True)  # Chỉ cho phép gửi ID voucher

    class Meta:
        model = VoucherUser
        fields = '__all__'

    def to_representation(self, instance):
        """
        Tùy chỉnh phản hồi để bao gồm thông tin chi tiết của user và voucher.
        """
        representation = super().to_representation(instance)
        # representation['user'] = UserSerializer(instance.user).data  # Serialize thông tin chi tiết của user
        representation['voucher'] = VoucherSerializer(instance.voucher).data  # Serialize thông tin chi tiết của voucher
        return representation
