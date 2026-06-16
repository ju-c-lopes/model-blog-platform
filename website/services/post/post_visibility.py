from django.db.models import QuerySet
from django.http import Http404, HttpRequest

from website.models.post.PostModel import Post


def published_posts() -> QuerySet[Post]:
    """Posts visíveis em listagens públicas (home, busca)."""
    return Post.objects.filter(status=Post.PUBLISHED)


def user_can_view_post(request: HttpRequest, post: Post) -> bool:
    if post.status == Post.PUBLISHED:
        return True
    if not request.user.is_authenticated:
        return False
    if request.user.is_staff:
        return True
    return post.author.user_id == request.user.pk


def get_post_for_view(request: HttpRequest, url_slug: str) -> Post:
    """Retorna post para detail/reactions; 404 se rascunho e visitante não autorizado."""
    post = (
        Post.objects.select_related("author")
        .prefetch_related("tags", "likes", "loves")
        .filter(url_slug=url_slug)
        .first()
    )
    if post is None or not user_can_view_post(request, post):
        raise Http404("Post não encontrado.")
    return post
