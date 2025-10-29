from django.urls import path  # Import path từ django.urls

import vnpay_python.views
from .views import * 
urlpatterns = [
    path('', vnpay_python.views.index, name='index'),  # Thay url bằng path
    path('payment', PaymentView.as_view(), name='payment'),
    path('payment_ipn', vnpay_python.views.payment_ipn, name='payment_ipn'),
    path('payment_return/', PaymentDetail.as_view(), name='payment_return'),
    path('query', vnpay_python.views.query, name='query'),
    path('refund', vnpay_python.views.refund, name='refund'),
]
