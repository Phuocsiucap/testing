from django.db import models


class Payment(models.Model):
    order_id = models.CharField(max_length=100, unique=True)  # Mã hóa đơn thanh toán
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # Số tiền
    order_desc = models.TextField(blank=True)  # Nội dung đơn hàng
    transaction_no = models.CharField(max_length=100, unique=True)  # Số giao dịch
    response_code = models.CharField(max_length=10)  # Mã phản hồi từ VNPAY
    pay_date = models.CharField(max_length=14)  # Ngày thanh toán (định dạng: yyyyMMddHHmmss)
    bank_code = models.CharField(max_length=20, blank=True)  # Mã ngân hàng
    card_type = models.CharField(max_length=50, blank=True)  # Loại thẻ
    tmn_code = models.CharField(max_length=50, blank=True)  # Mã TMN từ VNPAY
    checksum_valid = models.BooleanField(default=False)  # Trạng thái kiểm tra checksum
    created_at = models.DateTimeField(auto_now_add=True)  # Thời gian tạo
    updated_at = models.DateTimeField(auto_now=True)  # Thời gian cập nhật

    def __str__(self):
        return f"Payment(order_id={self.order_id}, amount={self.amount})"
