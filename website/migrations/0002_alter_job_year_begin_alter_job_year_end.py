# Generated by Django 5.0.3 on 2024-03-17 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='year_begin',
            field=models.IntegerField(max_length=4),
        ),
        migrations.AlterField(
            model_name='job',
            name='year_end',
            field=models.IntegerField(blank=True, max_length=4, null=True),
        ),
    ]