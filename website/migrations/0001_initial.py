# Generated by Django 5.0.3 on 2024-03-17 16:00

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(blank=True, max_length=45, null=True)),
                ('access_level', models.IntegerField(choices=[(1, 'Author'), (2, 'Reader')], default=2)),
                ('history', models.TextField(blank=True, max_length=1000, null=True)),
                ('current_job', models.TextField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Author',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occupation', models.CharField(blank=True, max_length=50, null=True)),
                ('month_begin', models.IntegerField(choices=[(1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'), (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'), (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')], default=1)),
                ('year_begin', models.PositiveIntegerField(max_length=4)),
                ('month_end', models.IntegerField(blank=True, choices=[(1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'), (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'), (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')], null=True)),
                ('year_end', models.PositiveIntegerField(blank=True, max_length=4, null=True)),
                ('current_job', models.BooleanField(blank=True, default=False, null=True)),
                ('roles_description', models.TextField(blank=True, max_length=300, null=True)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='website.author')),
            ],
            options={
                'db_table': 'Job',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('url_slug', models.TextField(default=uuid.uuid4, max_length=70, unique=True)),
                ('text', models.TextField()),
                ('published_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='website.author')),
            ],
            options={
                'db_table': 'Post',
            },
        ),
        migrations.AddField(
            model_name='author',
            name='written_posts',
            field=models.ManyToManyField(blank=True, db_column='pk', related_name='+', to='website.post'),
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reader_name', models.CharField(blank=True, max_length=45, null=True)),
                ('access_level', models.IntegerField(default=2)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='')),
                ('saved_posts', models.ManyToManyField(blank=True, db_column='pk', to='website.post')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Reader',
            },
        ),
    ]