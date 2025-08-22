from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone


from website.forms.PostForm import PostForm
from website.models.AuthorModel import Author
from website.models.PostModel import Post


@login_required
def create_post(request):
    """View for creating a new blog post"""
    # Check if the user has an author profile
    try:
        author = Author.objects.get(user=request.user)
    except Author.DoesNotExist:
        messages.error(request, "You need an author profile to create posts.")
        return redirect("home")

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # Create post but don't save to DB yet
            post = form.save(commit=False)
            # Set additional fields
            post.author = author
            post.published_date = timezone.now()
            post.updated_date = timezone.now()
            # Save to DB
            post.save()

            messages.success(request, "Your blog post has been created successfully!")
            return redirect("post_detail", url_slug=post.url_slug)
    else:
        form = PostForm()

    return render(request, "post/create_post.html", {"form": form})


@login_required
def edit_post(request, url_slug):
    """View for editing an existing blog post"""
    try:
        post = Post.objects.get(url_slug=url_slug)
    except Post.DoesNotExist:
        messages.error(request, "Post not found.")
        return redirect("home")

    # Check if the user is the author of the post
    if post.author.user != request.user:
        messages.error(request, "You do not have permission to edit this post.")
        return redirect("post_detail", url_slug=post.url_slug)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            # Update the post
            updated_post = form.save(commit=False)
            updated_post.updated_date = timezone.now()
            updated_post.save()

            messages.success(request, "Your blog post has been updated successfully!")
            return redirect("post_detail", url_slug=updated_post.url_slug)
    else:
        form = PostForm(instance=post)

    return render(request, "post/edit_post.html", {"form": form, "post": post})
