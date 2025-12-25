# portal/models/academic_years.py
from django.db import models

class AcademicYear(models.Model):
    code = models.CharField(max_length=20, unique=True)  # VD: 2024-2025
    name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name or self.code
