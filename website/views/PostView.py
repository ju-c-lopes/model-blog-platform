from django.shortcuts import render, get_object_or_404
from website.models.PostModel import Post

def post_detail(request, url_slug):
    # Get the post by its URL slug or return 404 if not found
    post = get_object_or_404(Post, url_slug=url_slug)
    return render(request, 'post/post_detail.html', {'post': post})