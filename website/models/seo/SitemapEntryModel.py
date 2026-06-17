from django.db import models


class SitemapEntry(models.Model):
    INCLUDE = "include"
    EXCLUDE = "exclude"

    ENTRY_TYPE_CHOICES = [
        (INCLUDE, "Incluir"),
        (EXCLUDE, "Excluir"),
    ]

    path = models.CharField(max_length=500, unique=True, help_text="Caminho da URL, ex.: /post/meu-slug/")
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPE_CHOICES)
    lastmod = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Opcional. Usado apenas em entradas do tipo Incluir.",
    )
    changefreq = models.CharField(max_length=20, blank=True)
    priority = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    notes = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "SitemapEntry"
        ordering = ("path",)

    def __str__(self):
        return f"{self.get_entry_type_display()}: {self.path}"


class SitemapHealthCheck(models.Model):
    path = models.CharField(max_length=500, unique=True)
    status_code = models.PositiveSmallIntegerField()
    checked_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "SitemapHealthCheck"
        ordering = ("path",)

    def __str__(self):
        return f"{self.path} → {self.status_code}"
