from django.db import models
from website.models import *
from website.models.AuthorModel import Author
import uuid


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url_slug = models.TextField(max_length=70, blank=False, null=False, unique=True, default=uuid.uuid4)
    meta_description = models.CharField(max_length=160, blank=True, null=True, help_text="SEO meta description (max 160 characters)")
    text = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
        
    class Meta:
        db_table = 'Post'
