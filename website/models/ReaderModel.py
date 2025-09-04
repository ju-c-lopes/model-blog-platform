from django.db import models

from website.models import User

# from django.dispatch import receiver


class Reader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reader_name = models.CharField(max_length=45, blank=True, null=True)
    access_level = models.IntegerField(default=2)
    saved_posts = models.ManyToManyField("Post", db_column="pk", blank=True)

    created_at = models.DateField(auto_now_add=True)

    image = models.ImageField(null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.reader_name}"

    # Quando houver um post na classe User, deverá ser chamado o método create_user_profile

    # Ao criar este método, já foi criado o superuser, por isso o uso do try
    # para não quebrar o app ao fazer login com admin

    """@receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        try:
            if created:
                Reader.objects.create(user=instance)
        except:
            raise "Não foi possível criar o usuário."

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        try:
            instance.reader.save()
        except:
            pass"""

    class Meta:
        db_table = "Reader"
