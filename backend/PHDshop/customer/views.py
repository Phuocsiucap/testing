from django.http import HttpResponse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import UserSerializer



class UserProfileView(APIView):
    # Không cần thêm `permission_classes` ở đây nếu middleware đã xác thực
    def get(self, request):
        if not request.user:
            return Response({'error': 'Unauthorized'}, status=401)

        # Lấy thông tin người dùng từ request.user
        user_data = UserSerializer(request.user)
        print("hello")

        print("hi")
        return Response({'user': user_data.data}, status=200)

class CreateUserView(APIView):
    permission_classes = [AllowAny]  #Cho phép tất cả người dùng truy cập
    print(6)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserView(APIView):
    
    def put(self, request):
        #Dữ liệu người dùng đã đăng nhập từ request.user
        user = request.user
        print("ahhh")
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
         #Dữ liệu người dùng đã đăng nhập từ request.user
        user = request.user
        print("bad")
        print(user)
        serializer = UserSerializer(user, data=request.data, partial=True)   #partial=True cho phép cập nhật một phần

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]  
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = User.objects.get(email=email)
            if user.password == password:
                serializer=UserSerializer(user)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)  
                refresh_token = str(refresh) 
                print(f"Access Token: {access_token}")
                return Response(
                    {
                    "message": "Login successful!",
                    "user":serializer.data,
                    "access_token": access_token,
                    "refresh_token": refresh_token 
                    }, 
                    status=status.HTTP_200_OK
                    )
            else:
                return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)
        



#   FOR POINT
import json 
from django.http import JsonResponse


def submit_score(request, username):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            score = int(data.get('score', 0))

            # Tìm User bằng email
            user = User.objects.get(email=username)
            user.loyaltyPoints += score
            user.save()

            return JsonResponse({"message": "Score updated successfully!", "loyaltyPoints": user.loyaltyPoints})
        except User.DoesNotExist:
            return JsonResponse({"error": f"User with email '{username}' not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == 'GET':
        try:
            # Trả về thông tin loyaltyPoints của user
            user = User.objects.get(email=username)
            return JsonResponse({"email": username, "loyaltyPoints": user.loyaltyPoints})
        except User.DoesNotExist:
            return JsonResponse({"error": f"User with email '{username}' not found"}, status=404)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


# FOR ADDRESS
from .models import Address
from .serializers import AddressSerializer


class AddressList(APIView):

    def get(self, request):
        """
        Retrieve all addresses for the authenticated user.
        """
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new address for the authenticated user.
        """
        data = request.data
        data['user'] = request.user.id  # Set the user to the current logged-in user
        
        # Nếu địa chỉ mới được đánh dấu là mặc định, cần đảm bảo không có địa chỉ nào khác là mặc định
        if data.get('is_default', False):
            # Cập nhật tất cả địa chỉ của người dùng thành không phải mặc định
            Address.objects.filter(user=request.user, is_default=True).update(is_default=False)

        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class AddressDetail(APIView):

    def get_object(self, ID, user):
        try:
            return Address.objects.get(id=ID, user=user)
        except Address.DoesNotExist:
            return None

    def get(self, request, id):
        """
        Retrieve an address by ID for the authenticated user.
        """
        address = self.get_object(id, request.user)
        if address:
            serializer = AddressSerializer(address)
            return Response(serializer.data)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    def put(self, request, id):
        """
        Update an address by ID for the authenticated user.
        """
        address = Address.objects.get(id=id)
        if address:
            # Nếu người dùng cập nhật để đặt làm mặc định, cần phải cập nhật tất cả các địa chỉ cũ thành không phải mặc định
            if request.data.get('is_default', False):
                # Cập nhật tất cả các địa chỉ của người dùng thành không phải mặc định
                Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
            
            # Thêm 'user' vào dữ liệu trước khi truyền vào serializer
            request.data['user'] = request.user.id  # Đảm bảo user được gán cho địa chỉ

            serializer = AddressSerializer(address, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                print(serializer.errors)  # Log lỗi
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, id):
        """
        Delete an address by ID for the authenticated user.
        """
        address = self.get_object(id, request.user)
        if address:
            address.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
