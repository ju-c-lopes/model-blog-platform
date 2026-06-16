import os

from django.db import migrations


def configure_site(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    domain = os.environ.get("DJANGO_SITE_DOMAIN", "localhost:8000")
    Site.objects.update_or_create(
        pk=1,
        defaults={"domain": domain, "name": "Platform Blog"},
    )


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0007_alter_tag_icon"),
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.RunPython(configure_site, migrations.RunPython.noop),
    ]
