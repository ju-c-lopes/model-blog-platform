from django.db import models


class Job(models.Model):
    occupation = models.CharField(max_length=50, blank=True)
    employee = models.ForeignKey("Author", related_name="jobs", on_delete=models.CASCADE)
    company = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField(verbose_name="Data de início")
    end_date = models.DateField(blank=True, null=True, verbose_name="Data de término")
    current_job = models.BooleanField(default=False)
    roles_description = models.TextField(max_length=300, blank=True)

    class Meta:
        db_table = "Job"
        ordering = ["-start_date", "-pk"]
