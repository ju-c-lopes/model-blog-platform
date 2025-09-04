from django.contrib import messages
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render

from website.forms.EditAuthorForm import (
    EditAuthorForm,
    GraduationForm,
    SocialMediaForm,
    UserChangeForm,
)
from website.models import User
from website.models.__init__ import ACADEMIC_LEVEL, SOCIAL_MEDIA
from website.models.AuthorModel import Author
from website.models.AuthorSocialMediaModel import SocialMedia
from website.models.GraduationsModel import Graduation


def view_author_page(request, slug):
    author = get_object_or_404(Author, author_url_slug=slug)
    context = {
        "author": author,
        "author_connected": False,
        "social_media_index": SOCIAL_MEDIA,
        "graduations_level": ACADEMIC_LEVEL,
    }
    if request.user != author.user:
        return render(
            request, template_name="author/author.html", context=context, status=200
        )
    context["author_connected"] = True
    return render(
        request, template_name="author/author.html", context=context, status=200
    )


def edit_author_profile(request, slug):
    author = get_object_or_404(Author, author_url_slug=slug)
    author_social_media = author.social_media.all()
    form = EditAuthorForm(instance=author)
    user_form = UserChangeForm(instance=request.user)
    social_forms = []
    for social in author_social_media:
        social_forms.append(SocialMediaForm(instance=social))
    social_empty_form = SocialMediaForm()
    send_message = False

    # create formset factory here (safe even if GraduationFormSet defined later)
    GraduationFormSetLocal = inlineformset_factory(
        Author, Graduation, form=GraduationForm, extra=0, can_delete=True
    )

    if request.POST:
        # rebind user and author forms with POST data
        user_form = UserChangeForm(request.POST, instance=request.user)
        author_form = EditAuthorForm(request.POST, request.FILES, instance=author)

        # instantiate formset with POST (and FILES) and try to detect prefix
        prefix = None
        for k in request.POST.keys():
            if k.endswith("-TOTAL_FORMS") and "gradu" in k.lower():
                prefix = k.rsplit("-TOTAL_FORMS", 1)[0]
                break
        if prefix is None:
            for k in request.POST.keys():
                if k.endswith("-TOTAL_FORMS"):
                    prefix = k.rsplit("-TOTAL_FORMS", 1)[0]
                    break

        if prefix:
            graduation_formset = GraduationFormSetLocal(
                request.POST, request.FILES, instance=author, prefix=prefix
            )
        else:
            graduation_formset = GraduationFormSetLocal(
                request.POST, request.FILES, instance=author
            )

        # (debug logs removed)

        # rebind social forms with POST
        social_forms = []
        for social in author_social_media:
            social_forms.append(SocialMediaForm(request.POST, instance=social))

        author_request_post = check_request_post(request)
        if author_request_post is not None:
            if author.image != "" and author_request_post["image"] is not None:
                author.image.delete(save=True)
                author.image = author_request_post["image"]

        # validate forms
        forms_ok = True

        # (debug logs removed)

        # username conflict check
        username_conflict = False
        if author_request_post:
            username_conflict = bool(author_request_post.get("check_username_request"))
        if not user_form.is_valid() or username_conflict:
            forms_ok = False
            if username_conflict:
                messages.error(request, "Nome de usuário já está em uso.")

        if not author_form.is_valid():
            forms_ok = False

        # validate graduation formset
        if not graduation_formset.is_valid():
            forms_ok = False

        if forms_ok:
            # save user (handle password: preserve original if empty)
            original_password = request.user.password
            user = user_form.save(commit=False)
            pw = user_form.cleaned_data.get("password")
            if pw:
                user.set_password(pw)
            else:
                # preserve original hashed password
                user.password = original_password
            user.save()

            # save author
            author = author_form.save()

            # update social media entries
            if update_social_media(request, author_social_media):
                send_message = True
            # create new social media if requested
            if (
                author_request_post
                and author_request_post.get("new_social_addition")
                and not any(author_request_post.get("exclude_social_media", []))
            ):
                create_social_media(request, author_request_post)
                send_message = True
            # exclude if requested
            if author_request_post and any(
                author_request_post.get("exclude_social_media", [])
            ):
                exclude_social_media(request, author)
                send_message = True

            # save graduation formset (instance already saved)
            graduation_formset.instance = author
            graduation_formset.save()
            send_message = True

            if send_message:
                messages.success(request, "Dados atualizados com sucesso.")
            return redirect("author", slug=author.author_url_slug)
        else:
            # render page with errors (no redirect)
            context = {
                "socialEmptyForm": social_empty_form,
                "userForm": user_form,
                "authorForm": author_form,
                "socialForms": social_forms,
                "academic_levels": ACADEMIC_LEVEL,
                "graduation_formset": graduation_formset,
            }
            return render(
                request,
                template_name="edit-author/edit-author.html",
                context=context,
            )
    else:
        # GET: provide an empty/loaded formset instance
        graduation_formset = GraduationFormSetLocal(instance=author)

    context = {
        "socialEmptyForm": social_empty_form,
        "userForm": user_form,
        "authorForm": form,
        "socialForms": social_forms,
        "academic_levels": ACADEMIC_LEVEL,
        "graduation_formset": graduation_formset,
    }
    return render(
        request, template_name="edit-author/edit-author.html", context=context
    )


def check_request_post(request):
    author_post_request_data = None
    if request.POST:
        author_post_request_data = {
            "username": request.POST["username"],
            "name": request.POST["author_name"],
            "check_username_request": Author.objects.filter(
                user__username=request.POST["username"]
            )
            .exclude(user__id=request.user.id)
            .first(),
            "image": request.FILES.get("image", None),
            "new_social_addition": len(request.POST.getlist("social_media_profile"))
            > len(
                Author.objects.get(
                    user__username=request.POST["username"]
                ).social_media.all()
            ),
            "exclude_social_media": request.POST.getlist("exclude-social"),
        }

    return author_post_request_data


def check_user_form(request, author):
    user_form = UserChangeForm(request.POST, instance=request.user)
    author_user = check_request_post(request)
    username_free = author_user["check_username_request"] != author.user.username
    if (
        user_form.is_valid()
        and author_user["username"] != author.user.username
        and username_free
    ):
        user_author = get_object_or_404(User, id=author.user.id)
        user_author.username = author_user["username"]
        user_author.save()
    return username_free


def check_author_form(request, author):
    author_form = EditAuthorForm(request.POST, request.FILES, instance=author)
    check_post = check_request_post(request)
    if author_form.is_valid():
        author.author_name = check_post["name"]
        author.save()
        return True
    return False


def update_social_media(request, author_social_media):
    social_media_request_post = list(
        zip(
            request.POST.getlist("social_media"),
            request.POST.getlist("social_media_profile"),
        )
    )
    updated = False
    for i in range(len(author_social_media)):
        if (
            author_social_media[i].social_media != int(social_media_request_post[i][0])
        ) or (
            author_social_media[i].social_media_profile
            != social_media_request_post[i][1]
        ):
            author_social_media[i].social_media = social_media_request_post[i][0]
            author_social_media[i].social_media_profile = social_media_request_post[i][
                1
            ]
            author_social_media[i].save()
            updated = True
    return updated


def create_social_media(request, author_request_post):
    social_media_request_post = list(
        zip(
            request.POST.getlist("social_media"),
            request.POST.getlist("social_media_profile"),
        )
    )
    author = Author.objects.get(user__username=author_request_post["username"])
    social = author.social_media.all()

    for i in range(len(social), len(social_media_request_post)):
        new_social = SocialMedia.objects.create(
            user_social_media=author,
            social_media=social_media_request_post[i][0],
            social_media_profile=social_media_request_post[i][1],
        )
        new_social.save()
        author.social_media.add(new_social)


def exclude_social_media(request, author):
    exclusions = check_request_post(request)["exclude_social_media"]
    for exclude_request in exclusions:
        if exclude_request != "":
            social_media = author.social_media.get(
                social_media=exclude_request
            ).delete()


def set_graduation():
    pass


def edit_author(request, author_slug=None):
    """Wrapper to keep compatibility: delegate to edit_author_profile.

    If no author_slug is provided, use the logged-in user's author slug.
    """
    if not author_slug:
        if hasattr(request, "user") and getattr(request.user, "author", None):
            slug = request.user.author.author_url_slug
        else:
            # nothing sensible to edit; redirect to home
            return redirect("/")
    else:
        slug = author_slug
    return edit_author_profile(request, slug)
