from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Voucher, VoucherUser
from .serializers import VoucherSerializer, VoucherUserSerializer
from customer.models import User


class VoucherListView(APIView):
    """
    API để lấy danh sách voucher còn hiệu lực.
    """
    def get(self, request):
        vouchers = Voucher.objects.filter(is_active=True)  # Chỉ lấy các voucher còn hiệu lực
        serializer = VoucherSerializer(vouchers, many=True)
        return Response(serializer.data)

class RedeemVoucherView(APIView):
    """
    API để đổi voucher sử dụng điểm của người dùng.
    """
    def post(self, request, voucher_id):
        user = request.user  # Lấy người dùng từ request
        points = user.loyaltyPoints  # Điểm của người dùng
        quantity = 1

        try:
            voucher = Voucher.objects.get(id=voucher_id)
        except Voucher.DoesNotExist:
            return Response({"detail": "Voucher not found."}, status=status.HTTP_404_NOT_FOUND)

        # Kiểm tra nếu người dùng đã đổi voucher này
        if VoucherUser.objects.filter(user=user, voucher=voucher).exists():
            return Response({"detail": "You have already redeemed this voucher."}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra điều kiện đổi voucher
        total_points_required = voucher.points_required * quantity

        if points < total_points_required:
            return Response({"detail": "Not enough points to redeem this voucher."}, status=status.HTTP_400_BAD_REQUEST)
        
        if voucher.quantity < quantity:
            return Response({"detail": "Not enough vouchers available."}, status=status.HTTP_400_BAD_REQUEST)

        # Giảm điểm và cập nhật số lượng voucher
        user.loyaltyPoints -= total_points_required
        # voucher.quantity -= quantity
        user.save()
        voucher.save()

        # Tạo bản ghi trong VoucherUser
        voucher_user = VoucherUser.objects.create(
            user=user,
            voucher=voucher,
            points_used=total_points_required,
            quantity=quantity,
            status="Redeemed"
        )

        # Trả về thông tin voucher đã đổi
        voucher_user_serializer = VoucherUserSerializer(voucher_user)
        return Response(voucher_user_serializer.data, status=status.HTTP_201_CREATED)


class RedeemedVouchersView(APIView):
    """
    API để lấy danh sách voucher mà người dùng đã đổi.
    """
    def get(self, request):
        user = request.user  # Lấy người dùng từ request
        status_filter = request.query_params.get('status', None)
        if status_filter: 
            # Lọc các voucher đã đổi của người dùng theo status
            redeemed_vouchers = VoucherUser.objects.filter(user=user, status=status_filter)
        else: 
            # Lọc tất cả các voucher đã đổi của người dùng
            redeemed_vouchers = VoucherUser.objects.filter(user=user)
        # Kiểm tra nếu không có voucher đã đổi
        if not redeemed_vouchers.exists():
            return Response({"detail": "No redeemed vouchers found."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize danh sách voucher đã đổi
        serializer = VoucherUserSerializer(redeemed_vouchers, many=True)

        return Response(serializer.data)
