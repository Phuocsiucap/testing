import requests 

# URL của API backend để đăng nhập và nhận token
login_url = "http://127.0.0.1:1234/api/admin/login/"

# Thông tin đăng nhập của Admin
login_data = {
    "username": "admin",  # Thay thế với tên đăng nhập admin của bạn
    "password": "1234",  # Thay thế với mật khẩu admin của bạn
}

# Gửi yêu cầu POST để đăng nhập và lấy token
response = requests.post(login_url, json=login_data)

if response.status_code == 200:
    # Lấy token từ phản hồi
    tokens = response.json()
    access_token = tokens.get("access_token")  # Lấy access_token từ response
    print("Admin Access Token:", access_token)
else:
    print("Error:", response.status_code)
    exit()

# Gửi yêu cầu GET để lấy danh sách người dùng
admin_api_url = "http://127.0.0.1:1234/api/admin/users/"  # Đảm bảo URL API đúng

# Headers với Token của Admin
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

# Gửi yêu cầu GET
response = requests.get(admin_api_url, headers=headers)
print(response.json())
# Kiểm tra kết quả
# if response.status_code :
#     print("Danh sách người dùng:", response.json())
# else:
#     print("Lỗi:", response.status_code)