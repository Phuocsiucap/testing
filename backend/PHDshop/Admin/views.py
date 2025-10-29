from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate

class AdminLoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Kiểm tra thông tin đăng nhập
        user = authenticate(username=username, password=password)
        if user is None or not user.is_staff:
            raise AuthenticationFailed('Invalid credentials or not an admin')

        # Tạo JWT refresh và access token
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        })
