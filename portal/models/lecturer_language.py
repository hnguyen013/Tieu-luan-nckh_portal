# portal/models/lecturer_language.py
from django.db import models


class LecturerLanguage(models.Model):
    lecturer = models.ForeignKey(
        "portal.Lecturer",
        on_delete=models.CASCADE,
        related_name="languages",
    )

    language = models.CharField(max_length=100)   # VD: English, Japanese
    level = models.CharField(max_length=50)       # VD: B2, IELTS 6.5, TOEIC 800

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "portal_lecturer_language"
        ordering = ["language"]
        constraints = [
            models.UniqueConstraint(
                fields=["lecturer", "language"],
                name="uniq_lecturer_language",
            )
        ]

    def __str__(self) -> str:
        return f"{self.lecturer} - {self.language} ({self.level})"
