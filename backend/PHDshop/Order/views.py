
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Order, OrderGood, Good
from .serializers import OrderSerializer, OrderGoodSerializer
from good.serializer import GoodSerializer
import datetime
from Cart.models import CartGood
from Voucher.models import Voucher, VoucherUser
from vnpay_python.models import Payment
from Voucher.serializers import * 
# Đặt hàng (1 hoặc nhiều sản phẩm cùng lúc)
class CreateOrderAPI(APIView):
    
    def post(self, request):
        user = request.user  # Lấy thông tin người dùng từ user đang đăng nhập
        order_id = request.data.get('order_id')
        # purchase_date = request.data.get('purchase_date')
        shipping_address = request.data.get('shipping_address')
        cartgoods_id = request.data.get('goods_id')
        voucher_user_id = request.data.get('voucherUserId')
        pay_id = request.data.get('pay_id')
        pay = get_object_or_404(Payment, id = pay_id)
        if not all([user, shipping_address, cartgoods_id]):
            return Response({"error": "Thiếu thông tin bắt buộc"}, status=status.HTTP_400_BAD_REQUEST)

        voucher = None
        discount_percentage = 0
        if voucher_user_id != None:
            print(34)
            try:
                voucher_user = get_object_or_404(VoucherUser, pk=voucher_user_id)
                
                voucher = get_object_or_404(Voucher, pk=voucher_user.voucher.id)
                print(voucher)
                if voucher.quantity <= 0:
                    return Response({"error": "Voucher đã hết hạn hoặc không có sẵn"}, status=status.HTTP_400_BAD_REQUEST)
                discount_percentage = voucher.discount_percentage / 100.0  # Giả sử voucher có trường discount_percentage
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        total_amount = 0
        # Kiểm tra số lượng sản phẩm trong kho trước khi tạo đơn hàng
        for id in cartgoods_id:
            cartgood = get_object_or_404(CartGood, pk=id)
            good = cartgood.good
            quantity = cartgood.quantity  # Assuming quantity is part of CartGood

            # Kiểm tra số lượng sản phẩm có đủ không
            if good.amount < quantity:
                print(good.amount)
                return Response({"error": f"Sản phẩm {good.goodName} không đủ số lượng trong kho."}, status=status.HTTP_400_BAD_REQUEST)
            total_amount += float(good.price) * quantity


        # Cộng điểm cho người dùng (ví dụ: 1 điểm = 1% tổng số tiền)
        points_earned = int(total_amount * 0.0001)  # Giả sử 1% tổng giá trị đơn hàng là điểm thưởng
        user.loyaltyPoints += points_earned
        print("pluss : " , points_earned, " point")
        user.save()
        
        # Áp dụng phần trăm giảm giá từ voucher
        if discount_percentage > 0:
            total_amount *= (1 - discount_percentage)
        print(total_amount)
        # Tạo đơn hàng
        order = Order.objects.create(
            order_id = order_id,
            # purchase_date=purchase_date,
            shipping_status='Chờ xác nhận',
            total_amount=total_amount,
            shipping_address=shipping_address,
            pay = pay,
            user=user,
            voucher=voucher,
        )
        # Lưu các sản phẩm trong đơn hàng và giảm số lượng trong kho, xoa khoi gio hang
        for id in cartgoods_id:
            cartgood = get_object_or_404(CartGood, pk=id)
            good = cartgood.good
            quantity = cartgood.quantity  # Assuming quantity is part of CartGood

            # Tạo bản ghi trong OrderGood
            OrderGood.objects.create(order=order, good=good, quantity=quantity)

            # Cập nhật lại số lượng sản phẩm trong kho
            good.amount -= quantity
            good.save()
            cartgood.delete()

        if voucher:
            voucher.quantity -= 1
            voucher.save()
            # Optionally, update the voucher status if needed
            voucher_user.status = 'Expired'
            voucher_user.save()

        # Cộng điểm cho người dùng (ví dụ: 1 điểm = 1% tổng số tiền)
        points_earned = int(total_amount * 0.0001)  # Giả sử 1% tổng giá trị đơn hàng là điểm thưởng
        user.loyaltyPoints += points_earned
        print("pluss : " , points_earned, " point")
        user.save()

        
        return Response("Don hang cua ban da duoc dat thanh cong", status=status.HTTP_201_CREATED)


# def patch(self, request, id):
#         """
#         API cập nhật trạng thái voucher của người dùng khi sử dụng
#         """
#         try:
#             voucher = Voucher.objects.get(id=id)
#             if voucher.quantity <= 0:
#                 return Response({"detail": "Voucher đã hết"}, status=status.HTTP_400_BAD_REQUEST)


#             # Pass the data and the voucher instance to the serializer
#             serializer = VoucherUserSerializer(user = request.user.id , data=request.data)
            
#             if serializer.is_valid():
#                 voucher.quantity -= 1
#                 voucher.save()
#                 serializer.save()

#                 return Response({"detail": "Cập nhật thành công"}, status=status.HTTP_200_OK)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         except Voucher.DoesNotExist:
#             return Response({"detail": "Voucher không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
    
# Lấy thông tin chi ti-đơn hàng 
class OrderDetailAPI(APIView):
    def get(self, request, id):
        # Lấy thông tin đơn hàng dựa trên `pk`
        order = get_object_or_404(Order, order_id=id)
        if order.user != request.user:  # Kiểm tra xem đơn hàng có phải của người dùng hiện tại không
            return Response({"error": "Bạn không có quyền truy cập đơn hàng này."}, status=status.HTTP_403_FORBIDDEN)
            
        order_serializer = OrderSerializer(order)
            # Lấy thông tin của các sản phẩm trong đơn hàng
        order_goods = OrderGood.objects.filter(order=order)
       
        order_goods_serializer = OrderGoodSerializer(order_goods, many=True)
        # Lấy danh sách các sản phẩm (Good) liên quan đến đơn hàng từ OrderGood
        goods_in_order = Good.objects.filter(ordergood__order=order).distinct()

        # Serialize danh sách sản phẩm
        goods_serializer = GoodSerializer(goods_in_order, many=True)
            # Trả về thông tin đơn hàng và các sản phẩm kèm theo
        response_data = {
            "order": order_serializer.data,
            "order_good": order_goods_serializer.data,
            "good": goods_serializer.data
        }
        print(response_data)
        return Response(response_data, status=status.HTTP_200_OK)
    
class OrderListView(APIView):
    def get(self, request):
        # Lấy tất cả đơn hàng của người dùng hiện tại
        orders = Order.objects.filter(user=request.user)
        order_serializer = OrderSerializer(orders, many=True)
        return Response(order_serializer.data, status=status.HTTP_200_OK)

from django.utils.timezone import now
class CancelOrderAPI(APIView):
    def post(self, request, id):
        # Lấy thông tin đơn hàng
        order = get_object_or_404(Order, order_id=id)

        # Kiểm tra quyền sở hữu
        if order.user != request.user:
            return Response({"error": "Bạn không có quyền hủy đơn hàng này."}, status=status.HTTP_403_FORBIDDEN)

        # Kiểm tra trạng thái đơn hàng (chỉ cho phép hủy khi đang ở trạng thái 'Processing')
        if order.shipping_status != 'Chờ xác nhận':
            return Response({"error": "Không thể hủy đơn hàng đã xử lý."}, status=status.HTTP_400_BAD_REQUEST)

        # Lấy các sản phẩm trong đơn hàng
        order_goods = OrderGood.objects.filter(order=order)

        for order_good in order_goods:
            good = order_good.good
            # Hoàn trả số lượng sản phẩm
            good.amount += order_good.quantity
            good.save()

        # # Xóa các sản phẩm liên quan trong bảng OrderGood
        # order_goods.delete()

        # Xóa đơn hàng hoặc cập nhật trạng thái đơn hàng
        order.shipping_status = "Đã hủy"
        order.updated_order_time = now()
        order.save()

        return Response({"success": "Đơn hàng đã được hủy thành công."}, status=status.HTTP_200_OK)
"""

TẠO ĐƠN HÀNG
Dữ liệu nhận được từ font (cần bao gồn cả token)

{
    "shipping_address": "123 Đường ABC, Quận 1, TP.HCM",
    "goods": [
        {
            "good_id": 1,
            "quantity": 2
        },
        {
            "good_id": 3,
            "quantity": 1
        }
    ]
}

BACKEND TRA VÈ THONG TIN CỦA 1 DONA HÀNG CU THE
{
    "order": {
        "order_id": 1,
        "purchase_date": "2024-11-10",
        "shipping_status": "Processing",
        "total_amount": 150.0,
        "shipping_address": "123 Main St",
        "user": 1
        "admin": 2
    }
    "goods": [
        {
            "id": 1,
            "good": {
                id": 3,
                "name": "Sản phẩm C",
                "price": 100000
                ...
                # các tong tin của good
            },
            "quantity": 2
        },
        {
            "id": 2,
            "good": {
                #các thông tin của good
            },
            "quantity": 1
        }
    ]
}



BACKEND TRẢ VỀ THÔNG TIN CỦA TẤT CẢ DƠN HÀNG CÚA USER
[
  {
    "order_id": 1,
    "purchase_date": "2024-11-10",
    "shipping_status": "Processing",
    "total_amount": 150.0,
    "shipping_address": "123 Main St",
    "user": 1
    "admin": 2
  },
  {
    "order_id": 2,
    "purchase_date": "2024-11-12",
    "shipping_status": "Shipped",
    "total_amount": 200.0,
    "shipping_address": "456 Another St",
    "user": 1
    "admin": null
  }
]
"""