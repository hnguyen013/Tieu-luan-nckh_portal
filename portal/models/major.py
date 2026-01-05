from django.db import models


class Major(models.Model):
    name = models.CharField("Ngành", max_length=150, unique=True)

    class Meta:
        verbose_name = "Ngành"
        verbose_name_plural = "Ngành"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
