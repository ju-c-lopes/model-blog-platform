import math
import re

from django.db import models
from django.utils.text import slugify

from django.utils import timezone


class Post(models.Model):
    DRAFT = "draft"
    PUBLISHED = "published"

    STATUS_CHOICES = [
        (DRAFT, "Draft"),
        (PUBLISHED, "Published"),
    ]

    author = models.ForeignKey(
        "Author", related_name="written_posts", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    url_slug = models.SlugField(
        max_length=70, unique=True, blank=False, help_text="Short SEO-friendly URL slug"
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="SEO meta description (max 160 characters)",
    )
    text = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)

    series = models.ForeignKey(
        "Series", on_delete=models.SET_NULL, null=True, blank=True, related_name="posts"
    )
    series_order = models.PositiveIntegerField(null=True, blank=True)

    @property
    def reading_time(self):
        text = self.text or ""

        # remove HTML tags
        clean_text = re.sub('<[^<]+?>', '', text)

        words = clean_text.split()
        total_words = len(words)

        minutes = math.ceil(total_words / 200)

        return max(1, minutes)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Post"
