from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from website.forms.user.UserChangeForm import UserChangeForm
from website.forms.user.UserCreationForm import UserCreationForm
from website.models import User
from website.models.author.AuthorModel import Author
from website.models.author.AuthorSocialMediaModel import SocialMedia
from website.models.author.GraduationsModel import Graduation
from website.models.author.JobsModel import Job
from website.models.post.PostModel import Post
from website.models.post.PostReactionModel import PostReaction
from website.models.post.PostViewModel import PostView
from website.models.post.SeriesModel import Series
from website.models.user.ReaderModel import Reader


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
    list_select_related = ("author", "reader_profile")
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
            elif hasattr(obj, "reader_profile"):
                return "Reader"
            else:
                return "No Profile"
        except Exception:
            return "No Profile"

    get_profile_type.short_description = "Profile Type"

    def get_profile_name(self, obj):
        """Display the user's profile name"""
        if hasattr(obj, "author"):
            return obj.author.author_name or obj.username

        if hasattr(obj, "reader_profile"):
            return obj.reader_profile.reader_name or obj.username

        return obj.username

    get_profile_name.short_description = "Profile Name"


class GraduationInline(admin.TabularInline):
    model = Graduation
    extra = 1


class JobInline(admin.TabularInline):
    model = Job
    extra = 1


class SocialMediaInline(admin.TabularInline):
    model = SocialMedia
    extra = 1


class AuthorAdmin(admin.ModelAdmin):

    inlines = [
        JobInline,
        GraduationInline,
        SocialMediaInline
    ]


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "published_date",
        "updated_date",
    )
    search_fields = (
        "title",
        "meta_description",
    )
    list_filter = (
        "published_date",
        "series",
    )
    prepopulated_fields = {"url_slug": ("title",)}


class SeriesAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "author",
        "created_at",
    )

    search_fields = ("title",)


class PostViewAdmin(admin.ModelAdmin):

    readonly_fields = (
        "reader",
        "post",
        "viewed_at",
    )

    list_display = (
        "post",
        "reader",
        "viewed_at",
    )


admin.site.register(User, UserAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(SocialMedia)
admin.site.register(Graduation)
admin.site.register(Job)
admin.site.register(Post, PostAdmin)
admin.site.register(PostReaction)
admin.site.register(PostView, PostViewAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Reader)
