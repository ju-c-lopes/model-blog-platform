from django.db import migrations, models


def seed_tags(apps, schema_editor):
    Tag = apps.get_model("website", "Tag")
    defaults = [
        ("docker", "Docker"),
        ("python", "Python"),
        ("django", "Django"),
        ("seo", "SEO"),
        ("javascript", "JavaScript"),
        ("linux", "Linux"),
        ("git", "Git"),
        ("postgresql", "PostgreSQL"),
    ]
    for slug, name in defaults:
        Tag.objects.get_or_create(slug=slug, defaults={"name": name, "icon": ""})


def unseed_tags(apps, schema_editor):
    Tag = apps.get_model("website", "Tag")
    Tag.objects.filter(
        slug__in=[
            "docker",
            "python",
            "django",
            "seo",
            "javascript",
            "linux",
            "git",
            "postgresql",
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0003_post_likes_loves"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("slug", models.SlugField(max_length=50, unique=True)),
                (
                    "icon",
                    models.CharField(
                        blank=True,
                        help_text="Caminho relativo em static/, ex.: img/icons/tags/docker.png",
                        max_length=120,
                    ),
                ),
            ],
            options={
                "db_table": "Tag",
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="post",
            name="cover_image",
            field=models.ImageField(blank=True, null=True, upload_to="post_covers/"),
        ),
        migrations.AddField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(blank=True, related_name="posts", to="website.tag"),
        ),
        migrations.RunPython(seed_tags, unseed_tags),
    ]
