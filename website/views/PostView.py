from django.shortcuts import render, get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from website.models import ACADEMIC_LEVEL, SOCIAL_MEDIA
from website.models.PostModel import Post


@xframe_options_exempt
def post_detail(request, url_slug):
    # Get the post by its URL slug or return 404 if not found
    post = get_object_or_404(Post, url_slug=url_slug)
    context = {'post': post}
    context['author_connected'] = request.user == post.author.user
    context['graduations_level'] = ACADEMIC_LEVEL
    context['social_media_index'] = SOCIAL_MEDIA
    return render(request, 'post/post_detail.html', context)
