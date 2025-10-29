# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from good.models import Good,Category,Brand
from good.serializer import GoodSerializer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import json
class GoodListView(APIView):
    authentication_classes = [JWTAuthentication]  # Sử dụng JWTAuthentication
    permission_classes = [IsAuthenticated]  # Kiểm tra nếu người dùng đã đăng nhập

    # Lấy danh sách các sản phẩm
    def get(self, request):
        goods = Good.objects.all()
        serializer = GoodSerializer(goods, many=True)
        return Response(serializer.data)

    # Thêm sản phẩm mới
    # def post(self, request):
    #     print(request.data)
    #     image = request.FILES.get('image')
    #     if image:
    #         # Tạo đường dẫn lưu ảnh
    #         file_path = os.path.join('goods/', image.name)
    #         # Lưu ảnh vào thư mục MEDIA_ROOT
    #         saved_image_path = default_storage.save(file_path, ContentFile(image.read()))
    #         print(f"Ảnh đã lưu tại: {saved_image_path}")
    #     serializer = GoodSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        print(request.data)

        # Parse dữ liệu từ request.POST để lấy thông tin sản phẩm (bao gồm các trường như goodName, amount, price, v.v.)
        product_data = json.loads(request.POST.get('good'))  # 'good' là chuỗi JSON chứa thông tin sản phẩm
        print("Product Data:", product_data)

        good_name = product_data['goodName']
        amount = product_data['amount']
        price = product_data['price']
        specifications = product_data['specifications']
        brand_id = product_data['brand']
        category_id = product_data['category']

        # Lấy thông tin Category và Brand từ cơ sở dữ liệu
        category = Category.objects.get(id=category_id)
        brand = Brand.objects.get(id=int(brand_id))

        # Lấy ảnh từ request.FILES
        image = request.FILES.get('image')  # Đây là file ảnh gửi lên
        if image:
            # Kiểm tra và lưu ảnh vào thư mục media
            file_path = os.path.join('images/', image.name)
            saved_image_path = default_storage.save(file_path, ContentFile(image.read()))
            print(f"Ảnh đã lưu tại: {saved_image_path}")
        else:
            saved_image_path = None

        # Tạo sản phẩm mới với ảnh (nếu có)
        good = Good.objects.create(
            goodName=good_name,
            amount=amount,
            price=price,
            specifications=specifications,
            brand=brand,
            category=category,
            image=image if saved_image_path else None,  # Lưu ảnh nếu có
        )

        # Sử dụng serializer để trả về thông tin sản phẩm đã tạo
        serializer = GoodSerializer(good)
        
        # Trả về thông tin sản phẩm với mã trạng thái 200 OK
        return Response(serializer.data, status=status.HTTP_200_OK)
        

from django.shortcuts import get_object_or_404
class GoodDetailView(APIView):
    authentication_classes = [JWTAuthentication]  # Sử dụng JWTAuthentication
    permission_classes = [IsAuthenticated]  # Kiểm tra nếu người dùng đã đăng nhập

    # Lấy thông tin sản phẩm
    def get(self, request, pk):
        good = get_object_or_404(Good, pk=pk)
        serializer = GoodSerializer(good)
        return Response(serializer.data)

    # Cập nhật thông tin sản phẩm
    def put(self, request, pk):
        print("Request data:", request.data)  # In dữ liệu yêu cầu ra console
        good = get_object_or_404(Good, pk=pk)
        serializer = GoodSerializer(good, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # Cập nhật một phần thông tin sản phẩm
    def patch(self, request, pk):
        good = get_object_or_404(Good, pk=pk)
        serializer = GoodSerializer(good, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Xóa sản phẩm
    def delete(self, request, pk):
        good = get_object_or_404(Good, pk=pk)
        good.delete()
        return Response({"detail": "Good deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
