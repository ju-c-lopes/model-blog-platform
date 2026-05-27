from dataclasses import dataclass

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.db import transaction
from django.forms.models import BaseInlineFormSet
from django.shortcuts import get_object_or_404
from django.urls import reverse

from website.forms.author.EditAuthorForm import EditAuthorForm
from website.forms.author.author_edit_formsets import (
    GRADUATION_FORMSET_PREFIX,
    GraduationFormSet,
    JOB_FORMSET_PREFIX,
    JobFormSet,
    SOCIAL_FORMSET_PREFIX,
    SocialMediaFormSet,
)
from website.forms.user.UserChangeForm import UserChangeForm
from website.models import ACADEMIC_LEVEL
from website.models.author.AuthorModel import Author


@dataclass
class AuthorEditBundle:
    user_form: UserChangeForm
    author_form: EditAuthorForm
    social_formset: BaseInlineFormSet
    graduation_formset: BaseInlineFormSet
    job_formset: BaseInlineFormSet


def get_author_for_edit(slug: str) -> Author:
    return get_object_or_404(Author, author_url_slug=slug)


def can_edit(user, author: Author) -> bool:
    if not user.is_authenticated:
        return False
    return user == author.user


def build_bundle(request, author: Author) -> AuthorEditBundle:
    if request.method == "POST":
        return AuthorEditBundle(
            user_form=UserChangeForm(request.POST, instance=request.user),
            author_form=EditAuthorForm(
                request.POST, request.FILES, instance=author
            ),
            social_formset=SocialMediaFormSet(
                request.POST,
                request.FILES,
                instance=author,
                prefix=SOCIAL_FORMSET_PREFIX,
            ),
            graduation_formset=GraduationFormSet(
                request.POST,
                request.FILES,
                instance=author,
                prefix=GRADUATION_FORMSET_PREFIX,
            ),
            job_formset=JobFormSet(
                request.POST,
                request.FILES,
                instance=author,
                prefix=JOB_FORMSET_PREFIX,
            ),
        )

    return AuthorEditBundle(
        user_form=UserChangeForm(instance=request.user),
        author_form=EditAuthorForm(instance=author),
        social_formset=SocialMediaFormSet(
            instance=author, prefix=SOCIAL_FORMSET_PREFIX
        ),
        graduation_formset=GraduationFormSet(
            instance=author, prefix=GRADUATION_FORMSET_PREFIX
        ),
        job_formset=JobFormSet(instance=author, prefix=JOB_FORMSET_PREFIX),
    )


def bundle_is_valid(bundle: AuthorEditBundle) -> bool:
    return (
        bundle.user_form.is_valid()
        and bundle.author_form.is_valid()
        and bundle.social_formset.is_valid()
        and bundle.graduation_formset.is_valid()
        and bundle.job_formset.is_valid()
    )


def save_bundle(bundle: AuthorEditBundle, request) -> None:
    with transaction.atomic():
        user = bundle.user_form.save()
        if bundle.user_form.password_will_change():
            try:
                update_session_auth_hash(request, user)
            except Exception:
                pass

        bundle.author_form.save()
        bundle.social_formset.save()
        bundle.graduation_formset.save()
        bundle.job_formset.save()


def success_url(author: Author) -> str:
    return reverse("author", kwargs={"slug": author.author_url_slug})


def add_validation_messages(request, bundle: AuthorEditBundle) -> None:
    if bundle.user_form.errors:
        for field, errors in bundle.user_form.errors.items():
            for error in errors:
                messages.error(request, f"{field.capitalize()}: {error}")
    else:
        messages.error(request, "Erro ao atualizar os dados. Verifique os campos.")


def as_template_context(bundle: AuthorEditBundle) -> dict:
    return {
        "user_form": bundle.user_form,
        "author_form": bundle.author_form,
        "social_formset": bundle.social_formset,
        "graduation_formset": bundle.graduation_formset,
        "job_formset": bundle.job_formset,
        "academic_levels": ACADEMIC_LEVEL,
    }
