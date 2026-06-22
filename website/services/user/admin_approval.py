from django.contrib.auth import authenticate

from website.models.user.UserModel import User


def _resolve_superuser(identifier: str) -> User | None:
    identifier = identifier.strip()
    if not identifier:
        return None
    admin = User.objects.filter(username__iexact=identifier, is_superuser=True).first()
    if admin is None and "@" in identifier:
        admin = User.objects.filter(email__iexact=identifier, is_superuser=True).first()
    return admin


def verify_superuser_credentials(identifier: str, password: str) -> bool:
    if not identifier or not password:
        return False
    admin = _resolve_superuser(identifier)
    if admin is None:
        return False
    return authenticate(email=admin.email, password=password) is not None
