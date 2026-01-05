# portal/models/lecturer.py
from django.db import models


class Lecturer(models.Model):
    GENDER_CHOICES = [
        ("M", "Nam"),
        ("F", "Nữ"),
        ("O", "Khác"),
    ]

    STATUS_CHOICES = [
        ("working", "Đang công tác"),
        ("leave", "Nghỉ/Ngưng công tác"),
        ("retired", "Nghỉ hưu"),
    ]

    # Id: Django tự tạo (AutoField/BigAutoField tuỳ settings)

    mgv = models.CharField(max_length=20, unique=True)  # MGV (change from lecturer_id)
    full_name = models.CharField(max_length=255)        # HOTEN

    date_of_birth = models.DateField(null=True, blank=True)  # NGAYSINH (change from year_of_birth)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="M")  # GIOITINH

    email = models.EmailField(null=True, blank=True)   # EMAIL
    phone_number = models.CharField(max_length=30, null=True, blank=True)  # SDT

    academic_rank = models.CharField(max_length=120, null=True, blank=True)  # CHUCDANH
    address = models.CharField(max_length=255, null=True, blank=True)        # DIACHI

    avatar = models.ImageField(upload_to="lecturers/avatars/", null=True, blank=True)  # AVATAR

    faculty = models.ForeignKey(  # KHOA (change from faculty_id)
        "portal.Faculty",
        on_delete=models.PROTECT,
        related_name="lecturers",
        null=True,
        blank=True,
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="working")  # TINHTRANG
    is_active = models.BooleanField(default=True)  

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "portal_lecturer"
        ordering = ["mgv"]

    def __str__(self) -> str:
        return f"{self.mgv} - {self.full_name}"
