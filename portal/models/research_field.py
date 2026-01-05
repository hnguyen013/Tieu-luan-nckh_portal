from django.db import models


class ResearchField(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "portal_research_field"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
