# portal/models/students.py
from django.db import models
from .faculty import Faculty
from .course import Course


class Student(models.Model):
    """
    Sinh viên tham gia đề tài NCKH.
    Dùng làm master data để:
    - Gán vào đề tài (leader / member)
    - Hiển thị hồ sơ sinh viên (profile + danh sách đề tài)
    """

    GENDER_CHOICES = [
        ("M", "Nam"),
        ("F", "Nữ"),
        ("O", "Khác"),
    ]

    mssv = models.CharField("Mã sinh viên", max_length=20, unique=True)
    full_name = models.CharField("Họ tên", max_length=255)

    year_of_birth = models.PositiveIntegerField("Năm sinh", null=True, blank=True)
    gender = models.CharField(
        "Giới tính",
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
    )

    class_name = models.CharField("Lớp", max_length=100, blank=True)
    major = models.CharField("Ngành", max_length=150, blank=True)
    faculty = models.ForeignKey(
    Faculty,
    on_delete=models.PROTECT,
    related_name="students",
    verbose_name="Khoa",
    null=True,
    blank=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        related_name="students",
        verbose_name="Khóa học",
        null=True,
        blank=True,
    )
    email = models.EmailField("Email", blank=True)

    avatar = models.ImageField(
        "Ảnh đại diện",
        upload_to="students/avatars/",
        null=True,
        blank=True,
    )

    # Soft delete / ngừng sử dụng (SV đã tốt nghiệp, không còn theo dõi)
    is_active = models.BooleanField("Còn theo dõi", default=True)

    created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)
    updated_at = models.DateTimeField("Ngày cập nhật", auto_now=True)

    class Meta:
        verbose_name = "Sinh viên"
        verbose_name_plural = "Sinh viên"
        ordering = ["mssv"]

    def __str__(self) -> str:
        return f"{self.mssv} - {self.full_name}"
