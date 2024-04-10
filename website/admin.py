from django.contrib import admin
from .models.AuthorModel import Author
from .models.PostModel import Post
from .models.GraduationsModel import Graduation
from .models.JobsModel import Job
from .models.AuthorSocialMediaModel import SocialMedia
from .models.ReaderModel import Reader
from .models.UserModel import User
from website.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ("email", "phone_number", "username", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("username", "phone_number")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")})
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "phone_number", "password1", "password2")
        }),
    )
    search_fields = ("email", "phone_number")
    ordering = ("email", "phone_number")

admin.site.register(User, UserAdmin)
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Graduation)
admin.site.register(Job)
admin.site.register(SocialMedia)
admin.site.register(Reader)
