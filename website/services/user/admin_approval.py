from django.contrib.auth import authenticate

from website.models.user.UserModel import User


def verify_superuser_credentials(username: str, password: str) -> bool:
    if not username or not password:
        return False
    admin = User.objects.filter(username__iexact=username.strip(), is_superuser=True).first()
    if admin is None:
        return False
    return authenticate(email=admin.email, password=password) is not None
