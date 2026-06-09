from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    icon = models.CharField(
        max_length=120,
        blank=True,
        help_text="Caminho relativo em static/, ex.: img/icons/tags/docker.png",
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Tag"
        ordering = ["name"]
