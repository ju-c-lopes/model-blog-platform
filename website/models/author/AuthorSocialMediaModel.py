from django.db import models
from website.models import SOCIAL_MEDIA


class SocialMedia(models.Model):
    user_social_media = models.ForeignKey(
        "Author", on_delete=models.CASCADE, related_name="social_media"
    )
    social_media = models.IntegerField(choices=SOCIAL_MEDIA)
    social_media_profile = models.URLField(max_length=200)

    class Meta:
        db_table = "Social_Media"
        constraints = [
            models.UniqueConstraint(
                fields=["user_social_media", "social_media"],
                name="unique_author_social_media"
            )
        ]
