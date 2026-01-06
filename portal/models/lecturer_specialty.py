# portal/models/lecturer_specialty.py
from django.db import models


class LecturerSpecialty(models.Model):
    lecturer = models.ForeignKey(
        "portal.Lecturer",
        on_delete=models.CASCADE,
        related_name="specialties",
    )

    specialty = models.CharField(max_length=150)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "portal_lecturer_specialty"
        ordering = ["specialty"]
        constraints = [
            models.UniqueConstraint(
                fields=["lecturer", "specialty"],
                name="uniq_lecturer_specialty",
            )
        ]

    def __str__(self) -> str:
        return f"{self.lecturer} - {self.specialty}"
