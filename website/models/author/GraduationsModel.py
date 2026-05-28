from django.db import models

from website.models import ACADEMIC_LEVEL, STATUS_MAP


class Graduation(models.Model):
    graduation_level = models.IntegerField(choices=ACADEMIC_LEVEL)
    school = models.TextField(max_length=100, blank=True)
    course = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey("Author", related_name="graduations", on_delete=models.CASCADE)
    year_graduation = models.PositiveIntegerField(blank=True, null=True)
    concluded = models.BooleanField(default=False)

    @property
    def display_text(self):
        gender = self.author.get_gender_display()

        concluded, studying = STATUS_MAP[self.graduation_level][gender]

        if self.concluded:
            text = concluded
        else:
            text = studying

        result = f"{text} em {self.course} na {self.school}"

        if self.concluded and self.year_graduation:
            result += f" em {self.year_graduation}"

        return result

    def __str__(self):
        return f"{self.graduation_level or 'Nível'} — {self.course or ''}"

    def get_display_text(self):
        author = self.author
        gender = author.get_gender_display()

        concluded, studying = STATUS_MAP[self.graduation_level][gender]

        status = concluded if self.concluded else studying

        return f"{status} em {self.course}"

    class Meta:
        db_table = "Graduation"
        ordering = ["-graduation_level", "-year_graduation"]
