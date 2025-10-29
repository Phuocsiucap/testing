from django.db import models
from customer.models import User

class Voucher(models.Model):
    title = models.CharField(max_length=255)  # Tiêu đề voucher
    discount_percentage = models.FloatField()  # Phần trăm giảm giá
    min_order_value = models.IntegerField()  # Đơn tối thiểu
    points_required = models.IntegerField()  # Điểm yêu cầu để đổi
    quantity = models.IntegerField(default=0)  # Số lượng voucher còn lại
    is_active = models.BooleanField(default=True)  # Trạng thái voucher

    def __str__(self):
        return f"{self.title} - {self.discount_percentage}% giảm giá"


class VoucherUser(models.Model):
    # Liên kết với người dùng
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="redeemed_vouchers")

    # Liên kết với voucher đã đổi
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, related_name="voucher_users")

    # Số điểm đã sử dụng để đổi voucher
    points_used = models.IntegerField()

    # Số lượng voucher đã đổi
    quantity = models.IntegerField(default=1)

    # Thời gian đổi voucher
    redeemed_at = models.DateTimeField(auto_now_add=True)

    # Trạng thái voucher (Có thể có thêm logic để sử dụng)
    status = models.CharField(max_length=20, choices=[('redeemed', 'Redeemed'), ('expired', 'Expired')], default='redeemed')

    # Đảm bảo mỗi người dùng chỉ có thể đổi một voucher duy nhất
    class Meta:
        unique_together = ('user', 'voucher')  # Mỗi user chỉ có thể đổi mỗi voucher 1 lần

    def __str__(self):
        return f"{self.user.fullName} redeemed {self.voucher.title} on {self.redeemed_at}"
