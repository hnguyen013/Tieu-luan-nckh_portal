from django.db import models


class Course(models.Model):
    name = models.CharField("Khóa học", max_length=150, unique=True)

    class Meta:
        verbose_name = "Khóa học"
        verbose_name_plural = "Khóa học"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
