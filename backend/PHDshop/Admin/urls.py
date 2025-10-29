# urls.py
from django.urls import path
from .views import AdminLoginView
from .views_users import AdminUserManagementView, AdminUserTotal
from .views_goods import *
from .views_orders import *
from .views_orders import MonthlyRevenueAPIView, WeeklyRevenueAPIView

urlpatterns = [
    path('login/', AdminLoginView.as_view(), name='admin-login'),

    path('users/', AdminUserManagementView.as_view(), name='admin-user-list-create'),  # GET - Lấy danh sách người dùng, POST - Thêm người dùng mới
    path('users/<int:pk>/', AdminUserManagementView.as_view(), name='admin-user-update'),  # PUT - Cập nhật người dùng (toàn bộ)
    path('users/<int:pk>/partial/', AdminUserManagementView.as_view(), name='admin-user-partial-update'),  # PATCH - Cập nhật một phần thông tin người dùng
    path('users/<int:pk>/delete/', AdminUserManagementView.as_view(), name='admin-user-delete'),  # DELETE - Xóa người dùng


    path('goods/', GoodListView.as_view(), name='good-list'),  # Lấy danh sách và tạo mới
    path('goods/<int:pk>/', GoodDetailView.as_view(), name='good-detail'),  # Xem, cập nhật, xóa sản phẩm theo ID


    # Quản lý đơn hàng
    path('orders/', OrderListView.as_view(), name='order-list'),  # Lấy danh sách đơn hàng và tạo đơn hàng mới
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),  # Chi tiết, sửa và xóa đơn hàng

    # Quản lý sản phẩm trong đơn hàng
    path('orders/<int:order_pk>/goods/', OrderGoodListView.as_view(), name='order-good-list'),  # Lấy danh sách sản phẩm trong đơn hàng
    path('orders/<int:order_pk>/goods/add/', OrderGoodListView.as_view(), name='order-good-add'),  # Thêm sản phẩm vào đơn hàng
    
    path('revenue/monthly/', MonthlyRevenueAPIView.as_view(), name='monthly-revenue'),
    path('revenue/weekly/', WeeklyRevenueAPIView.as_view(), name='weekly-revenue'),
##

    path('total-users/', AdminUserTotal.as_view(), name='admin-total-users'),  # Đường dẫn cho API
    path('delivered-orders-count/', DeliveredOrdersCountAPIView.as_view(), name='delivered-orders-count'),
    path('today-revenue/', TodayRevenueAPIView.as_view(), name='today-revenue'),

]
