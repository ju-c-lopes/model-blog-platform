from django.db import models
from django.utils.text import slugify

from website.models import GENDER_CHOICE, ROLE_CHOICE
from website.models.user.UserModel import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="author")
    author_name = models.CharField(max_length=45, blank=False)
    gender = models.IntegerField(choices=GENDER_CHOICE, default=2)
    author_url_slug = models.SlugField(max_length=70, unique=True)
    access_level = models.IntegerField(choices=ROLE_CHOICE, default=2)
    history = models.TextField(max_length=2000, blank=True)

    created_at = models.DateField(auto_now_add=True)

    image = models.ImageField(null=True, blank=True, default=None)

    review = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Author Review",
        help_text="Short professional description about the author.",
    )

    @property
    def first_name(self):
        return self.author_name.split()[0]

    @property
    def current_job(self):
        return self.jobs.filter(current_job=True).first()

    @property
    def social_links(self):
        links = []

        for social in self.social_media.all():
            name = social.get_social_media_display().lower()

            links.append(
                {
                    "name": name,
                    "url": social.social_media_profile,
                    "icon": f"img/icons/{name}.png",
                }
            )

        return links

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.author_url_slug:
            self.author_url_slug = slugify(self.author_name)
        return super().save(*args, **kwargs)

    def get_social_media(self):
        return self.social_media.all()

    def get_graduations(self):
        return self.graduations.all().order_by("-year_graduation")

    def get_main_graduation(self):
        return self.graduations.order_by("-year_graduation").first()

    def get_jobs(self):
        return self.jobs.all().order_by("-year_begin", "-month_begin")

    def get_current_job(self):
        return self.jobs.filter(current_job=True).order_by("-year_begin", "-month_begin").first()

    def get_author_headline(self):
        job = self.get_current_job()
        graduation = self.get_main_graduation()

        parts = []

        if graduation:
            parts.append(graduation.get_display_text())

        if job:
            parts.append(job.title)

        return "\n".join(parts)

    class Meta:
        db_table = "Author"
