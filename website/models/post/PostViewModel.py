from django.db import models


class PostView(models.Model):

    reader = models.ForeignKey("Reader", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    viewed_at = models.DateTimeField(auto_now_add=True)
