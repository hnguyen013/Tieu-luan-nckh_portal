# portal/models/projects.py
from django.conf import settings
from django.db import models


class Project(models.Model):
    """
    Bảng PROJECT theo đúng skeleton:
    ID (AutoField PK)
    CODE, TITLE, PROJECT_LEVEL, RESEARCH_FIELD,
    HOST_ORGANIZATION, IMPLEMENTING_ORGANIZATION,
    SUMMARY, START_YEAR, END_YEAR, STATUS, BUDGET, CATEGORY, is_active
    """

    class Category(models.TextChoices):
        SAMPLE = "SAMPLE", "Mẫu / Prototype"
        SOFTWARE = "SOFTWARE", "Phần mềm / Hệ thống"
        PROCESS = "PROCESS", "Quy trình / Giải pháp"
        MATERIAL = "MATERIAL", "Tài liệu / Giáo trình"
        PAPER = "PAPER", "Bài báo khoa học"

    # CODE
    code = models.CharField(max_length=20, unique=True)

    # TITLE
    title = models.CharField(max_length=255)

    # PROJECT_LEVEL
    project_level = models.CharField(max_length=50)

    # RESEARCH_FIELD (nhập tay, không FK)
    research_field = models.CharField(max_length=100)

    # HOST_ORGANIZATION
    host_organization = models.CharField(max_length=255)

    # IMPLEMENTING_ORGANIZATION
    implementing_organization = models.CharField(max_length=255)

    # SUMMARY (VARCHAR 2000, nullable)
    summary = models.CharField(max_length=2000, null=True, blank=True)

    # START_YEAR / END_YEAR (Not Null)
    start_year = models.DateField()
    end_year = models.DateField()

    # STATUS (BOOLEAN default FALSE)
    status = models.BooleanField(default=False)

    # BUDGET (nullable)
    budget = models.FloatField(null=True, blank=True)

    # CATEGORY (Not Null)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.SAMPLE,
    )

    # is_active (soft delete / active flag)
    is_active = models.BooleanField(default=True)

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
        constraints = [
            models.UniqueConstraint(fields=["project", "lecturer"], name="uq_project_lecturer")
        ]


class ProjectStudent(models.Model):
    class Role(models.TextChoices):
        LEADER = "LEADER", "Trưởng nhóm"
        MEMBER = "MEMBER", "Thành viên"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_students")
    student = models.ForeignKey("portal.Student", on_delete=models.PROTECT)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["project", "student"], name="uq_project_student")
        ]


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
