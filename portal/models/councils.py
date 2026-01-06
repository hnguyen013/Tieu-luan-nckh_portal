# portal/models/councils.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Council(models.Model):
    """
    Council (Hội đồng chấm)
    """
    # council_id: Django tự tạo id (PK)

    project = models.OneToOneField(
        "portal.Project",
        on_delete=models.CASCADE,
        related_name="council",
    )  # project_id

    council_title = models.CharField(max_length=255)  # council_title
    grading_date = models.DateField(null=True, blank=True)  # grading_date
    notes = models.TextField(blank=True, default="")  # notes

    class Meta:
        ordering = ["-grading_date"]

    def __str__(self):
        return f"{self.council_title} ({self.project.code})"


class CouncilMember(models.Model):
    """
    CouncilMember (Thành viên hội đồng)
    """
    # id: Django tự tạo

    council = models.ForeignKey(
        "portal.Council",
        on_delete=models.CASCADE,
        related_name="members",
    )  # council_id

    lecturer = models.ForeignKey(
        "portal.Lecturer",
        on_delete=models.PROTECT,
        related_name="council_memberships",
    )  # lecturer_id

    role = models.CharField(max_length=50)  # role

    component_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )  # component_score

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["council", "lecturer"],
                name="uq_council_member",
            )
        ]

    def __str__(self):
        return f"{self.council_id} - {self.lecturer.mgv} ({self.role})"
