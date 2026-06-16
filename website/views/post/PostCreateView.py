import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt

from website.forms.post.PostForm import PostForm
from website.models.author.AuthorModel import Author
from website.models.post.PostModel import Post
from website.services.post import post_content_images as content_images


def _ensure_upload_session(request) -> str:
    session_id = request.session.get("post_content_upload_session")
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session["post_content_upload_session"] = session_id
        request.session.modified = True
    return session_id


def _selected_tag_ids(form, post) -> set[int]:
    if form.is_bound:
        return {int(pk) for pk in form.data.getlist("tags") if pk.isdigit()}
    if post:
        return set(post.tags.values_list("pk", flat=True))
    return set()


def _pending_new_tag_names(form) -> list[str]:
    if not form.is_bound:
        return []

    names = []
    seen = set()
    for raw_name in form.data.getlist("new_tag_names"):
        name = raw_name.strip()
        if not name:
            continue
        key = name.casefold()
        if key in seen:
            continue
        seen.add(key)
        names.append(name)
    return names


@xframe_options_exempt
@login_required
def edit_post(request, url_slug=None):
    """Unified view for editing an existing blog post or creating a new one"""
    post = None
    is_creating = url_slug is None
    author = None

    if not is_creating:
        try:
            post = Post.objects.prefetch_related("tags").get(url_slug=url_slug)
        except Post.DoesNotExist:
            messages.error(request, "Post not found.")
            return redirect("home")

        # Check if the user is the author of the post
        if post.author.user != request.user:
            messages.error(request, "You do not have permission to edit this post.")
            return redirect("post_detail", url_slug=post.url_slug)
    else:
        # Check if the user has an author profile for creating posts
        try:
            author = Author.objects.get(user=request.user)
        except Author.DoesNotExist:
            messages.error(request, "You need an author profile to create posts.")
            return redirect("home")

    if request.method == "POST":
        if is_creating:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.author = author
                if new_post.status == Post.PUBLISHED:
                    new_post.published_date = timezone.now().date()
                new_post.updated_date = timezone.now()

                upload_session_id = request.POST.get("upload_session_id", "").strip()
                session_id = request.session.get("post_content_upload_session")
                if upload_session_id and session_id and upload_session_id == session_id:
                    new_post.text = content_images.consolidate_temp_images(
                        new_post.text,
                        upload_session_id,
                        new_post.url_slug,
                    )
                    request.session.pop("post_content_upload_session", None)

                new_post.save()
                form.save_m2m()
                messages.success(request, "Post criado com sucesso!")
                return redirect("post_detail", url_slug=new_post.url_slug)
        else:
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                updated_post = form.save()
                messages.success(request, "Post atualizado com sucesso!")
                return redirect("post_detail", url_slug=updated_post.url_slug)
    else:
        form = PostForm(instance=post) if post else PostForm()

    selected_tag_ids = _selected_tag_ids(form, post)
    pending_new_tag_names = _pending_new_tag_names(form)
    upload_session_id = _ensure_upload_session(request) if is_creating else ""

    return render(
        request,
        "blog/pages/post/edit_post.html",
        {
            "form": form,
            "post": post,
            "is_creating": is_creating,
            "available_tags": form.fields["tags"].queryset,
            "selected_tag_ids": selected_tag_ids,
            "pending_new_tag_names": pending_new_tag_names,
            "upload_session_id": upload_session_id,
        },
    )
