import uuid

from django.conf import settings
from django.db import models

from website.models import *
from website.models.AuthorModel import Author
from website.utils.sanitizer import sanitize_html


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url_slug = models.TextField(
        max_length=70, blank=False, null=False, unique=True, default=uuid.uuid4
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        null=True,
        help_text="SEO meta description (max 160 characters)",
    )
    text = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    # Users who liked this post
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="liked_posts"
    )
    # Users who loved this post
    loves = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="loved_posts"
    )

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        # Sanitize rich text before saving to avoid stored XSS
        try:
            self.text = sanitize_html(self.text)
        except Exception:
            # If sanitizer fails for any reason, fall back to original text
            pass
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Post"
