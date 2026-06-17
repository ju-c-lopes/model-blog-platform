from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0009_publish_existing_posts"),
    ]

    operations = [
        migrations.CreateModel(
            name="SitemapEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "path",
                    models.CharField(help_text="Caminho da URL, ex.: /post/meu-slug/", max_length=500, unique=True),
                ),
                (
                    "entry_type",
                    models.CharField(
                        choices=[("include", "Incluir"), ("exclude", "Excluir")],
                        max_length=10,
                    ),
                ),
                (
                    "lastmod",
                    models.DateTimeField(
                        blank=True,
                        help_text="Opcional. Usado apenas em entradas do tipo Incluir.",
                        null=True,
                    ),
                ),
                ("changefreq", models.CharField(blank=True, max_length=20)),
                ("priority", models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
                ("notes", models.CharField(blank=True, max_length=255)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "SitemapEntry",
                "ordering": ("path",),
            },
        ),
        migrations.CreateModel(
            name="SitemapHealthCheck",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("path", models.CharField(max_length=500, unique=True)),
                ("status_code", models.PositiveSmallIntegerField()),
                ("checked_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "SitemapHealthCheck",
                "ordering": ("path",),
            },
        ),
    ]
