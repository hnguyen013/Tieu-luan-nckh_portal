# portal/models/course.py
from django.db import models


class Course(models.Model):
    """
    Danh mục Khóa học (K45, K46,...)
    Dùng để gán cho sinh viên, lọc theo khóa trên giao diện tra cứu.
    """

    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Mã khóa",
        help_text="Ví dụ: K45, K46..."
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Tên khóa",
        help_text="Ví dụ: Khóa 45 (2023–2027)"
    )
    start_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Năm bắt đầu"
    )
    end_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Năm kết thúc"
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
        verbose_name = "Khóa học"
        verbose_name_plural = "Danh mục khóa học"
        ordering = ["sort_order", "code"]

    def __str__(self):
        # Ví dụ: "K45 - Khóa 45 (2023–2027)"
        if self.name:
            return f"{self.code} - {self.name}"
        return self.code
