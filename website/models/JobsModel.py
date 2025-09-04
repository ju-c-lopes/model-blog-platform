from django.db import models

from website.models import *
from website.models.AuthorModel import Author


class Job(models.Model):
    occupation = models.CharField(max_length=50, blank=True, null=True)
    employee = models.OneToOneField(Author, on_delete=models.CASCADE)
    month_begin = models.IntegerField(choices=MONTH_CHOICE, default=1)
    year_begin = models.PositiveIntegerField()
    month_end = models.IntegerField(choices=MONTH_CHOICE, blank=True, null=True)
    year_end = models.PositiveIntegerField(blank=True, null=True)
    current_job = models.BooleanField(blank=True, null=True, default=False)
    roles_description = models.TextField(max_length=300, blank=True, null=True)

    class Meta:
        db_table = "Job"
