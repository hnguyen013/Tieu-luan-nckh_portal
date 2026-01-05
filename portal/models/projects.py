# portal/models/projects.py
from django.conf import settings
from django.db import models


class Project(models.Model):
    class Status(models.TextChoices):
        PROPOSED = "PROPOSED", "Đề xuất"
        REVIEWING = "REVIEWING", "Đang xét duyệt"
        IN_PROGRESS = "IN_PROGRESS", "Đang thực hiện"
        ACCEPTED = "ACCEPTED", "Đã nghiệm thu"
        REJECTED = "REJECTED", "Không duyệt"

    class Category(models.TextChoices):
        SAMPLE = "SAMPLE", "Mẫu / Prototype"
        SOFTWARE = "SOFTWARE", "Phần mềm / Hệ thống"
        PROCESS = "PROCESS", "Quy trình / Giải pháp"
        MATERIAL = "MATERIAL", "Tài liệu / Giáo trình"
        PAPER = "PAPER", "Bài báo khoa học"

    # Mapping theo bảng DETAI
    code = models.CharField(max_length=20, unique=True)   # MADETAI
    title = models.CharField(max_length=255)              # TENDETAI

    # Các field mới thêm -> để nullable để khỏi lỗi migrate khi DB đã có row
    project_level = models.CharField(max_length=50, null=True, blank=True)  # CAPDETAI

    research_field = models.ForeignKey(  # LINHVUC
        "portal.ResearchField",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    host_organization = models.CharField(  # DONVICHUTRI
        max_length=255,
        null=True,
        blank=True,
    )
    implementing_organization = models.CharField(  # DONVITHUCHIEN
        max_length=255,
        null=True,
        blank=True,
    )

    # NOIDUNG
    summary = models.TextField(blank=True)

    # MUCTIEU
    objectives = models.CharField(max_length=1000, null=True, blank=True)

    # KINHPHI
    budget = models.FloatField(null=True, blank=True)

    # PHANLOAI (có default -> không bị hỏi khi migrate)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.SAMPLE,
    )

    # NAMBATDAU / NAMKETTHUC (nullable để khỏi bị hỏi)
    start_year = models.DateField(null=True, blank=True)
    end_year = models.DateField(null=True, blank=True)

    # Trạng thái hệ thống + soft delete
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PROPOSED)
    is_active = models.BooleanField(default=True)

    # FK hệ thống
    faculty = models.ForeignKey("portal.Faculty", on_delete=models.PROTECT)
    academic_year = models.ForeignKey("portal.AcademicYear", on_delete=models.PROTECT)
    project_type = models.ForeignKey("portal.ProjectType", on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_projects",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "portal_project"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.title}"


class ProjectLecturer(models.Model):
    """
    GV hướng dẫn (1 hoặc nhiều) - through để mở rộng vai trò (GV chính/đồng hướng dẫn).
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_lecturers")
    lecturer = models.ForeignKey("portal.Lecturer", on_delete=models.PROTECT)
    role = models.CharField(max_length=50, default="Hướng dẫn")

    class Meta:
        unique_together = ("project", "lecturer")


class ProjectStudent(models.Model):
    class Role(models.TextChoices):
        LEADER = "LEADER", "Trưởng nhóm"
        MEMBER = "MEMBER", "Thành viên"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_students")
    student = models.ForeignKey("portal.Student", on_delete=models.PROTECT)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)

    class Meta:
        unique_together = ("project", "student")


def project_upload_path(instance, filename):
    return f"projects/{instance.project.code}/{filename}"


class ProjectAttachment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to=project_upload_path)
    original_name = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )


class ProjectStatusLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="status_logs")
    from_status = models.CharField(max_length=20, blank=True)
    to_status = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    note = models.CharField(max_length=255, blank=True)
