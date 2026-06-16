from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_POST

from website.services.post.post_search import resolve_posts_back_url
from website.services.post.post_visibility import get_post_for_view


@xframe_options_exempt
def post_detail(request, url_slug):
    try:
        post = get_post_for_view(request, url_slug)
    except Http404:
        raise Http404("Post não encontrado.") from None
    context = {
        "post": post,
        "posts_back_url": resolve_posts_back_url(request),
        "is_draft_preview": post.status == post.DRAFT,
    }
    if request.user.is_authenticated:
        context["user_liked"] = post.likes.filter(pk=request.user.pk).exists()
        context["user_loved"] = post.loves.filter(pk=request.user.pk).exists()
    else:
        context["user_liked"] = False
        context["user_loved"] = False
    return render(request, "blog/pages/post/post_detail.html", context)


@require_POST
def toggle_like(request, url_slug):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Authentication required")
    try:
        post = get_post_for_view(request, url_slug)
    except Http404:
        return JsonResponse({"error": "Post não encontrado."}, status=404)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
        # ensure user can't both like and love simultaneously (optional)
        if user in post.loves.all():
            post.loves.remove(user)
    return JsonResponse(
        {
            "liked": liked,
            "loved": post.loves.filter(pk=user.pk).exists(),
            "likes_count": post.likes.count(),
            "loves_count": post.loves.count(),
        }
    )


@require_POST
def toggle_love(request, url_slug):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Authentication required")
    try:
        post = get_post_for_view(request, url_slug)
    except Http404:
        return JsonResponse({"error": "Post não encontrado."}, status=404)
    user = request.user
    if user in post.loves.all():
        post.loves.remove(user)
        loved = False
    else:
        post.loves.add(user)
        loved = True
        if user in post.likes.all():
            post.likes.remove(user)
    return JsonResponse(
        {
            "loved": loved,
            "liked": post.likes.filter(pk=user.pk).exists(),
            "loves_count": post.loves.count(),
            "likes_count": post.likes.count(),
        }
    )
