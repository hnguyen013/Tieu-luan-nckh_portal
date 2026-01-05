from django.db import models


class Faculty(models.Model):
    name = models.CharField("Khoa", max_length=150, unique=True)

    class Meta:
        verbose_name = "Khoa"
        verbose_name_plural = "Khoa"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
