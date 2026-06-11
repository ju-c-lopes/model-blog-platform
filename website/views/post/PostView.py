from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_POST

from website.models.post.PostModel import Post


@xframe_options_exempt
def post_detail(request, url_slug):
    post = get_object_or_404(
        Post.objects.select_related("author").prefetch_related("tags", "likes", "loves"),
        url_slug=url_slug,
    )
    context = {"post": post}
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
    post = get_object_or_404(Post, url_slug=url_slug)
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
    post = get_object_or_404(Post, url_slug=url_slug)
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
