from django.urls import path
from .views import VoucherListView, RedeemVoucherView, RedeemedVouchersView

urlpatterns = [
    path('', VoucherListView.as_view(), name='voucher_list'),
    path('redeem/<int:voucher_id>/', RedeemVoucherView.as_view(), name='redeem-voucher'),
    path('redeemed_vouchers/', RedeemedVouchersView.as_view(), name='redeemed_vouchers'),
    path('redeemed_vouchers/<int:id>', RedeemedVouchersView.as_view(), name='redeemed_vouchers'),
]