# portal/models/lecturer.py
from django.db import models


class Lecturer(models.Model):
    GENDER_CHOICES = [
        ("M", "Nam"),
        ("F", "Nữ"),
        ("O", "Khác"),
    ]

    lecturer_id = models.CharField(max_length=30, unique=True)  # Mã GV
    full_name = models.CharField(max_length=255)

    year_of_birth = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="M")

    faculty = models.ForeignKey(
        "portal.Faculty",
        on_delete=models.PROTECT,
        related_name="lecturers",
        null=True,
        blank=True,
    )

    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)

    academic_rank = models.CharField(max_length=120, null=True, blank=True)  # Chức danh
    degree = models.CharField(max_length=120, null=True, blank=True)         # Học vị

    avatar = models.ImageField(upload_to="lecturers/avatars/", null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "portal_lecturer"
        ordering = ["lecturer_id"]

    def __str__(self) -> str:
        return f"{self.lecturer_id} - {self.full_name}"
