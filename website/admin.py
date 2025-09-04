from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from website.forms import UserChangeForm, UserCreationForm

from .models.AuthorModel import Author
from .models.AuthorSocialMediaModel import SocialMedia
from .models.GraduationsModel import Graduation
from .models.JobsModel import Job
from .models.PostModel import Post
from .models.ReaderModel import Reader
from .models.UserModel import User

# Register your models here.


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = (
        "email",
        "phone_number",
        "username",
        "is_staff",
        "get_profile_type",
        "get_profile_name",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("username", "phone_number")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "phone_number", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email", "phone_number")
    ordering = ("email", "phone_number")

    def get_profile_type(self, obj):
        """Display the user's profile type"""
        try:
            if hasattr(obj, "author"):
                return "Author"
            elif hasattr(obj, "reader"):
                return "Reader"
            else:
                return "No Profile"
        except Exception:
            return "No Profile"

    get_profile_type.short_description = "Profile Type"

    def get_profile_name(self, obj):
        """Display the user's profile name"""
        try:
            if hasattr(obj, "author") and obj.author.author_name:
                return obj.author.author_name
            elif hasattr(obj, "reader") and obj.reader.reader_name:
                return obj.reader.reader_name
            else:
                return obj.username
        except Exception:
            return obj.username

    get_profile_name.short_description = "Profile Name"


admin.site.register(User, UserAdmin)
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Graduation)
admin.site.register(Job)
admin.site.register(SocialMedia)
admin.site.register(Reader)
