from django.db import models


class Series(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    author = models.ForeignKey("Author", related_name="series", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(
        upload_to="series_covers/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Series"
        ordering = ["-created_at"]
