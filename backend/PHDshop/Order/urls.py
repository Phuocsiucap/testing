from django.urls import path
from .views import CreateOrderAPI, OrderDetailAPI,OrderListView,CancelOrderAPI

urlpatterns = [
    path('', CreateOrderAPI.as_view(), name='place-order'),  # Đặt hàng
    path('order_list/', OrderListView.as_view(), name='order-list'),  # Xem danh sách đơn hàng của người dùng
    path('order_detail/<int:id>/', OrderDetailAPI.as_view(), name='order-detail'),  # Xem chi tiết đơn hàng
    path('cancel_order/<int:id>/',CancelOrderAPI.as_view(), name='order-cancel')
]

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