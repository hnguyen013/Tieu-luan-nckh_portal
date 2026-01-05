# portal/models/students.py
from django.db import models
from .faculty import Faculty
from .course import Course
from .major import Major



class Student(models.Model):
    """
    Sinh viên (theo ràng buộc lý thuyết + dùng bảng Khoa/Khóa học riêng)
    """

    GENDER_CHOICES = [
        ("M", "Nam"),
        ("F", "Nữ"),
    ]

    STATUS_CHOICES = [
        ("studying", "Đang học"),
        ("leave", "Nghỉ"),
        ("reserved", "Bảo lưu"),
        ("graduated", "Tốt nghiệp"),
    ]

    # Nếu bạn vẫn muốn MSV riêng (đang dùng nhiều trong UI/form) thì GIỮ
    mssv = models.CharField("Mã sinh viên", max_length=20, unique=True)

    # HOTEN: theo lý thuyết thường max 100
    full_name = models.CharField("Họ tên", max_length=100)

    # NGAYSINH: DateField NOT NULL
    date_of_birth = models.DateField("Ngày sinh")

    # GIOITINH: NOT NULL, chỉ M/F
    gender = models.CharField("Giới tính", max_length=1, choices=GENDER_CHOICES)

    # DIACHI: nullable
    address = models.CharField("Địa chỉ liên hệ", max_length=255, null=True, blank=True)

    # EMAIL: NOT NULL + UNIQUE
    email = models.EmailField("Email", max_length=100, unique=True)

    # MANGANH: NOT NULL
    major = models.ForeignKey(
    Major,
    on_delete=models.PROTECT,
    related_name="students",
    verbose_name="Ngành",
    )   

    # KHOA: FK bảng Faculty (không bắt buộc xóa được -> PROTECT)
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.PROTECT,
        related_name="students",
        verbose_name="Khoa",
    )

    # KHOAHOC: FK bảng Course
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="students",
        verbose_name="Khóa học",
    )

    # TINHTRANG: NOT NULL (dùng choices)
    status = models.CharField("Tình trạng", max_length=20, choices=STATUS_CHOICES, default="studying")
    is_active = models.BooleanField("Còn theo dõi", default=True)


    avatar = models.ImageField(
        "Ảnh đại diện",
        upload_to="students/avatars/",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Sinh viên"
        verbose_name_plural = "Sinh viên"
        ordering = ["mssv"]

    def __str__(self) -> str:
        return f"{self.mssv} - {self.full_name}"
