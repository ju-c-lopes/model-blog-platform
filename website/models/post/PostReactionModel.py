from django.db import models
from django.conf import settings
from website.models.post.PostModel import Post


class PostReaction(models.Model):

    LIKE = "like"
    LOVE = "love"

    REACTION_CHOICES = [
        (LIKE, "Like"),
        (LOVE, "Love"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="reactions"
    )

    reaction = models.CharField(
        max_length=10,
        choices=REACTION_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")
