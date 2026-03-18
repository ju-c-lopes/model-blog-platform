from django.db import models
from website.models.user.UserModel import User


class Reader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="reader_profile")
    saved_posts = models.ManyToManyField("Post", related_name="saved_by_readers", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="readers", null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        db_table = "Reader"
