from website.models import *
from django.db import models
from website.models.AuthorModel import Author


class Graduation(models.Model):
    graduation_level = models.IntegerField(choices=ACADEMIC_LEVEL, blank=True, null=True)
    course = models.TextField(max_length=200, blank=True, null=True)
    school = models.TextField(max_length=100, blank=True, null=True)
    student = models.ForeignKey(Author, related_name='graduations', on_delete=models.CASCADE)
    year_graduation = models.PositiveIntegerField(blank=True, null=True)
    concluded = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self):
        return f"{self.graduation_level or 'Nível'} — {self.course or ''}"
