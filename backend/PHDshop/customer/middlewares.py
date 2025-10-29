from django.shortcuts import render

# Create your views here.
import jwt
from datetime import datetime
from django.http import JsonResponse
from customer.models import User
from customer.serializers import UserSerializer
from PHDshop.settings import SECRET_KEY
# Secret key dùng để giải mã JWT

def verify_jwt(token):
    try:
        # Giải mã token và kiểm tra tính hợp lệ của nó
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        # Kiểm tra xem token có hết hạn hay không
        exp_timestamp = decoded_token.get('exp')
        if exp_timestamp and exp_timestamp < datetime.now().timestamp():
            return None  # Token đã hết hạn

        # Nếu token hợp lệ, trả về thông tin của người dùng
        return decoded_token

    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None


def get_user_from_token(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return None


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lấy token từ header Authorization
        auth_header = request.headers.get('Authorization')
        # Kiểm tra nếu là admin API và bỏ qua xác thực
        if request.path.startswith('/api/admin/'):
            return self.get_response(request)

        if auth_header:
            token = auth_header.split(' ')[1]  # Lấy token từ "Bearer <token>"

            user_data = verify_jwt(token)
            if user_data:
                # Gán thông tin người dùng vào request để sử dụng sau này
                user = get_user_from_token(user_data['user_id'])
                if user:
                    # serializer = UserSerializer(user)
                    request.user = user
                    return self.get_response(request)
                else:
                    print('sad')
                    return JsonResponse({'detail': 'User not found'}, status=404)
            else:
                print("bad")
                return JsonResponse({'detail': 'Invalid or expired token'}, status=401)

        # Nếu không có token hoặc token không hợp lệ, bỏ qua xác thực
        return self.get_response(request)


class DisableCSRFMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        return self.get_response(request)
