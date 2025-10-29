from django.urls import path
from .views import CartAPI, CreateCartGoodAPI, CartGoodAPI, RemoveGoodFromCartAPI
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # Lấy chi tiết giỏ hàng
    path('', CartAPI.as_view(), name='cart-detail'),

    # Thêm sản phẩm vào giỏ hàng
    path('add/', CreateCartGoodAPI.as_view(), name='cart-add-good'),

    # Cập nhật số lượng sản phẩm trong giỏ hàng
    # path('update/', CartGoodAPI.as_view(), name='cart-update-good'),
    path('update/<int:cart_good_id>/', CartGoodAPI.as_view(), name='cart-update-good'),

    # Xóa sản phẩm khỏi giỏ hàng
    # path('remove/', RemoveGoodFromCartAPI.as_view(), name='cart-remove-good'),
    path('remove/<int:cart_good_id>/', RemoveGoodFromCartAPI.as_view(), name='cart-remove-good'),
]



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


THÊM VÀO GIỎI
thêm vào giỏ cần gửi
{
  "good_id": 10,
  "quantity": 2
}
kèm token




CẬP NHẬT CẦN GỬI
{
  "good_id": 10,
  "quantity": 2
}
kèm token



XÓA CẦN GỬI token

"""