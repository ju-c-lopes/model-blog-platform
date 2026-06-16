from django.db import migrations


def publish_existing_posts(apps, schema_editor):
    Post = apps.get_model("website", "Post")
    Post.objects.filter(status="draft").update(status="published")


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0008_configure_site"),
    ]

    operations = [
        migrations.RunPython(publish_existing_posts, migrations.RunPython.noop),
    ]
