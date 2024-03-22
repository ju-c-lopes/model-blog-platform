from django.contrib import admin
from .models.AuthorModel import Author
from .models.PostModel import Post
from .models.GraduationsModel import Graduation
from .models.JobsModel import Job
from .models.AuthorSocialMediaModel import SocialMedia
from .models.ReaderModel import Reader

# Register your models here.

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Graduation)
admin.site.register(Job)
admin.site.register(SocialMedia)
admin.site.register(Reader)
