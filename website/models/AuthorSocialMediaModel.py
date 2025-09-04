from django.db import models

from website.models import SOCIAL_MEDIA


class SocialMedia(models.Model):
    user_social_media = models.ForeignKey(
        "Author", blank=False, null=False, unique=False, on_delete=models.CASCADE
    )
    social_media = models.IntegerField(choices=SOCIAL_MEDIA, blank=True, null=True)
    social_media_profile = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "Social_Media"
