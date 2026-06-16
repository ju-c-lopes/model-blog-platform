import unicodedata

from website.models.author.AuthorModel import Author
from website.models.user.ReaderModel import Reader
from website.models.user.UserModel import User


def treat_accentuation(name: str) -> str:
    if not name:
        return ""
    normalized = unicodedata.normalize("NFD", name)
    return normalized.encode("ascii", "ignore").decode("utf-8")


def generate_username(display_name: str) -> str:
    cleaned = treat_accentuation(display_name).strip()
    prefix = cleaned.split()[0].lower() if cleaned else "user"
    cont = User.objects.count() + 1
    base = f"{prefix}-user{cont}"
    username = base
    suffix = 1
    while User.objects.filter(username__iexact=username).exists():
        username = f"{base}-{suffix}"
        suffix += 1
    return username


def build_author_slug(author_name: str) -> str:
    author_name_replaced = treat_accentuation(author_name)
    parts = [p for p in author_name_replaced.split(" ") if p]
    if not parts:
        parts = ["autor"]
    slug = "-".join(p.lower() for p in parts[:-1])
    if parts:
        last = parts[-1].lower()
        slug = f"{slug}-{last}" if slug else last
    candidate = slug
    suffix = 1
    while Author.objects.filter(author_url_slug=candidate).exists():
        candidate = f"{slug}-{suffix}"
        suffix += 1
    return candidate


def create_author_profile(user: User, author_name: str) -> Author:
    author = Author(
        user=user,
        author_name=author_name,
        author_url_slug=build_author_slug(author_name),
        access_level=1,
    )
    author.save()
    return author


def create_reader_profile(user: User, reader_name: str) -> Reader:
    reader = Reader(user=user, reader_name=reader_name or "")
    reader.save()
    return reader
