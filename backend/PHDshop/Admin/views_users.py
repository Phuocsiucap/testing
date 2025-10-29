from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from customer.models import User as CustomUser
from customer.serializers import UserSerializer as CustomUserSerializer

class AdminUserManagementView(APIView):
    authentication_classes = [JWTAuthentication]  # Sử dụng JWTAuthentication
    permission_classes = [IsAuthenticated]  # Kiểm tra nếu người dùng đã đăng nhập

    # Lấy danh sách người dùng
    def get(self, request):
        # Kiểm tra nếu người dùng có quyền Admin
        

        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    # Thêm người dùng mới
    def post(self, request):
        

        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Sửa thông tin người dùng
    def put(self, request, pk):
        

        try:
            user = CustomUser.objects.get(pk=pk)
            serializer = CustomUserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    # Cập nhật một phần thông tin người dùng
    def patch(self, request, pk):
        

        try:
            user = CustomUser.objects.get(pk=pk)
            serializer = CustomUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    # Xóa người dùng
    def delete(self, request, pk):
        

        try:
            user = CustomUser.objects.get(pk=pk)
            user.delete()
            return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

#Hùng sửa
class AdminUserTotal(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):  # Đảm bảo phương thức GET có mặt ở đây
        total_users = CustomUser.objects.count()
        return Response({"total_users": total_users}, status=status.HTTP_200_OK)