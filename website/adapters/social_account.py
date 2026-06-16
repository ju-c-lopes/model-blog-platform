from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from website.models.author.AuthorModel import Author
from website.models.user.ReaderModel import Reader
from website.models.user.UserModel import User
from website.services.user.user_registration import generate_username


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return
        email = sociallogin.user.email or sociallogin.account.extra_data.get("email")
        if not email:
            return
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return
        sociallogin.connect(request, user)

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        display_name = data.get("name") or data.get("given_name") or user.email.split("@")[0]
        user.username = generate_username(display_name)
        return user

    def save_user(self, request, sociallogin, form=None):
        user = sociallogin.user
        if not user.pk:
            user.set_unusable_password()
        user = super().save_user(request, sociallogin, form)
        if not Author.objects.filter(user=user).exists():
            display_name = sociallogin.account.extra_data.get("name") or user.username
            Reader.objects.get_or_create(
                user=user,
                defaults={"reader_name": display_name},
            )
        return user
