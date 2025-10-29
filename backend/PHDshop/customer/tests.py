from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

# Sử dụng get_user_model() để lấy model User của bạn
User = get_user_model()

# Lấy user từ database (đảm bảo rằng đây là instance của User)
user = User.objects.get(email="user@example.com")

# Đảm bảo rằng user là instance của User và tạo token
token, created = Token.objects.get_or_create(user=user)

print(token)