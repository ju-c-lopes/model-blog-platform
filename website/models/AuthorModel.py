from website.models import *
import uuid

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=45, blank=True, null=True)
    author_url_slug = models.TextField(max_length=70, blank=False, null=False, unique=True, default=uuid.uuid4)
    access_level = models.IntegerField(choices=ROLE_CHOICE, default=1)
    written_posts = models.ManyToManyField('Post', db_column='pk', blank=True, related_name='+')
    graduations = models.ManyToManyField('Graduation', db_column='pk', blank=True, related_name='+')
    history = models.TextField(max_length=1000, blank=True, null=True)
    jobs = models.ManyToManyField('Job', db_column='pk', blank=True, related_name='+')
    social_media = models.ManyToManyField('SocialMedia', blank=True, related_name='+')
    
    created_at = models.DateField(auto_now_add=True)

    image = models.ImageField(null=True, blank=True, default=None)

    def __str__(self):
        return f'{self.user.username}'
    
    # Quando houver um post na classe User, deverá ser chamado o método create_user_profile

    # Ao criar este método, já foi criado o superuser, por isso o uso do try
    # para não quebrar o app ao fazer login com admin
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        try:
            if created:
                Author.objects.create(user=instance)
        except:
            pass
    
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        try:
            instance.author.save()
        except:
            pass

    class Meta:
        db_table = 'Author'
