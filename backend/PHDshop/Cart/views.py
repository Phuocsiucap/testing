from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartGood
from .serializers import CartSerializer, CartGoodSerializer
from django.shortcuts import get_object_or_404
from good.models import Good

class CartAPI(APIView):

    def get(self, request):
        try:
            # Lấy hoặc tạo giỏ hàng của người dùng
            cart, created = Cart.objects.get_or_create(
                user=request.user
            )

            # Lấy tất cả sản phẩm trong giỏ
            cart_goods = CartGood.objects.filter(cart=cart)

            # Serialize dữ liệu
            cart_serializer = CartSerializer(cart)
            cart_goods_serializer = CartGoodSerializer(cart_goods, many=True)

            # Trả về dữ liệu giỏ hàng cùng với các sản phẩm
            return Response({
                'cart': cart_serializer.data,
                'cart_goods': cart_goods_serializer.data,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Xử lý lỗi bất ngờ
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""
lấy thông tin giỏ hàng(gửi token)
{
  "cart": {
        "id": 1,
        "user": 5,
        "note": "asdflaksd"
  },
  "cart_goods": [
    {
      "id": 1,
      "cart": 1,
      "good": {
            #thong tin các thuoc tinh của good
      }
      "quantity": 2
    },
    {
      "id": 2,
      "cart": 1,
      "good": {
            #thong tin các thuoc tinh của good
      }
      "quantity": 1
    }
  ]
}
"""


class CreateCartGoodAPI(APIView):
    
    # Thêm sản phẩm vào giỏ hàng
    def post(self, request):
        cart,_ = Cart.objects.get_or_create(user = request.user)  # Lấy giỏ hàng của người dùng hiện tại, neu chua co tao ms 
        good_id = request.data.get('good_id')  # ID của sản phẩm cần thêm vào giỏ
        quantity = request.data.get('quantity', 1)  # Số lượng mặc định là 1 nếu không cung cấp

        if quantity <= 0:
            return Response({"detail": "Số lượng sản phẩm phải lớn hơn 0."}, status=status.HTTP_400_BAD_REQUEST)

        # Lấy sản phẩm từ cơ sở dữ liệu
        good = get_object_or_404(Good, id=good_id)

        # Kiểm tra xem sản phẩm có còn trong kho không
        if good.amount == 0:
            return Response({"detail": "Sản phẩm này đã hết hàng."}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra xem sản phẩm đã có trong giỏ hàng của người dùng chưa
        try:
            cart_good = CartGood.objects.get(cart=cart, good=good)
            # Nếu sản phẩm đã có trong giỏ, cập nhật số lượng
            cart_good.quantity += quantity
            cart_good.save()
            return Response({"messege": "Thêm thành công"}, status=status.HTTP_200_OK)
        except CartGood.DoesNotExist:
            # Nếu sản phẩm chưa có trong giỏ, tạo mới
            serializer = CartGoodSerializer(data={'cart': cart.id, 'good': good.id, 'quantity': quantity})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
"""
thêm vào giỏ cần gửi
{
  "good_id": 10,
  "quantity": 2
}
kèm token

"""


class CartGoodAPI(APIView):
    

    # Cập nhật số lượng sản phẩm trong giỏ hàng
    def patch(self, request,cart_good_id):
        # cart = get_object_or_404(Cart, user=request.user)
        cart_good = get_object_or_404(CartGood, id=cart_good_id, cart__user=request.user)
        print(request.data)
        # good_id = request.data.get('good_id')
        new_quantity = request.data.get('quantity')

        # if not good_id or new_quantity is None:
        #     return Response({"detail": "Cần cung cấp mã sản phẩm và số lượng."}, status=status.HTTP_400_BAD_REQUEST)

        # cart_good = get_object_or_404(CartGood, cart=cart, good_id=good_id)

        # Kiểm tra tồn kho trước khi thay đổi số lượng
        # good = get_object_or_404(Good, id=good_id)
        # good=cart_good.good
        # if good.amount == 0:  # Nếu sản phẩm đã hết hàng
        #     return Response({"detail": "Sản phẩm này hiện đã hết hàng."}, status=status.HTTP_400_BAD_REQUEST)

        # if good.amount < new_quantity:
        #     return Response({"detail": "Sản phẩm này không đủ số lượng trong kho."}, status=status.HTTP_400_BAD_REQUEST)

        # Nếu số lượng mới hợp lệ, cập nhật giỏ hàng
        # if new_quantity <= 0:
        #     cart_good.delete()
        #     return Response(status=status.HTTP_204_NO_CONTENT)

        cart_good.quantity = new_quantity
        cart_good.save()
        serializer = CartGoodSerializer(cart_good)
        return Response(serializer.data, status=status.HTTP_200_OK)

"""
CẬP NHẬT CẦN GỬI

  "good_id": 10,
  "quantity": 2
}
kèm token

"""

class RemoveGoodFromCartAPI(APIView):
    
    def delete(self, request, cart_good_id):
        # Lấy thông tin sản phẩm trong giỏ hàng dựa trên ID và người dùng
        cart_good = get_object_or_404(CartGood, id=cart_good_id, cart__user=request.user)

        # Xóa sản phẩm
        cart_good.delete()

        # Trả về phản hồi thành công
        return Response({"message": "Cart item removed successfully."}, status=status.HTTP_204_NO_CONTENT)

'''
gửi tokent
'''











"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from .models import Cart, Good, CartGood
from .serializers import CartGoodSerializer

class CreateCartGoodAPI(APIView):
    
    def post(self, request):
        # Lấy token từ header
        token = request.headers.get('Authorization')
        if not token:
            return Response({"detail": "Token không được cung cấp."}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra token có hợp lệ không
        try:
            token = token.split(" ")[1]  # Tách "Bearer <token>"
            access_token = AccessToken(token)
            user = User.objects.get(id=access_token['user_id'])  # Lấy người dùng từ token
        except Exception as e:
            return Response({"detail": "Token không hợp lệ."}, status=status.HTTP_403_FORBIDDEN)

        cart = get_object_or_404(Cart, user=user)  # Lấy giỏ hàng của người dùng hiện tại
        good_id = request.data.get('good_id')  # ID của sản phẩm cần thêm vào giỏ
        quantity = request.data.get('quantity', 1)  # Số lượng mặc định là 1 nếu không cung cấp

        if quantity <= 0:
            return Response({"detail": "Số lượng sản phẩm phải lớn hơn 0."}, status=status.HTTP_400_BAD_REQUEST)

        # Lấy sản phẩm từ cơ sở dữ liệu
        good = get_object_or_404(Good, id=good_id)

        # Kiểm tra xem sản phẩm có còn trong kho không
        if good.amount == 0:
            return Response({"detail": "Sản phẩm này đã hết hàng."}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra xem sản phẩm đã có trong giỏ hàng của người dùng chưa
        try:
            cart_good = CartGood.objects.get(cart=cart, good=good)
            # Nếu sản phẩm đã có trong giỏ, cập nhật số lượng
            cart_good.quantity += quantity
            cart_good.save()
            return Response({"messege": "Thêm thành công"}, status=status.HTTP_200_OK)
        except CartGood.DoesNotExist:
            # Nếu sản phẩm chưa có trong giỏ, tạo mới
            serializer = CartGoodSerializer(data={'cart': cart.id, 'good': good.id, 'quantity': quantity})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""