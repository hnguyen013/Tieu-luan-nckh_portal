from django.db import models


class Faculty(models.Model):
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Mã khoa",
        help_text="Ví dụ: CNTT, TOAN, VAN..."
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Tên khoa",
        help_text="Ví dụ: Khoa Công nghệ Thông tin"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Đang sử dụng"
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Thứ tự hiển thị"
    )

    class Meta:
        verbose_name = "Khoa"
        verbose_name_plural = "Danh mục khoa"
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name
