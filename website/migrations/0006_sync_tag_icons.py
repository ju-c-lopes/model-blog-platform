from django.db import migrations

from website.utils.tag_catalog import TAG_DEFINITIONS


def sync_tags(apps, schema_editor):
    Tag = apps.get_model("website", "Tag")
    for slug, name, icon in TAG_DEFINITIONS:
        Tag.objects.update_or_create(slug=slug, defaults={"name": name, "icon": icon})


def unsync_tags(apps, schema_editor):
    Tag = apps.get_model("website", "Tag")
    slugs = [slug for slug, _name, _icon in TAG_DEFINITIONS]
    Tag.objects.filter(slug__in=slugs).update(icon="")


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0005_alter_job_options"),
    ]

    operations = [
        migrations.RunPython(sync_tags, unsync_tags),
    ]
