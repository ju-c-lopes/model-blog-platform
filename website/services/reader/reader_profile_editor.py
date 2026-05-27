from dataclasses import dataclass

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse

from website.forms.user.EditReaderForm import EditReaderForm
from website.forms.user.UserChangeForm import UserChangeForm
from website.models.user.ReaderModel import Reader


@dataclass
class ReaderEditBundle:
    user_form: UserChangeForm
    reader_form: EditReaderForm


def get_reader_for_edit(user) -> Reader:
    return get_object_or_404(Reader, user=user)


def can_edit(user, reader: Reader) -> bool:
    if not user.is_authenticated:
        return False
    return user == reader.user


def build_bundle(request, reader: Reader) -> ReaderEditBundle:
    if request.method == "POST":
        return ReaderEditBundle(
            user_form=UserChangeForm(request.POST, instance=request.user),
            reader_form=EditReaderForm(
                request.POST, request.FILES, instance=reader
            ),
        )

    return ReaderEditBundle(
        user_form=UserChangeForm(instance=request.user),
        reader_form=EditReaderForm(instance=reader),
    )


def bundle_is_valid(bundle: ReaderEditBundle) -> bool:
    return bundle.user_form.is_valid() and bundle.reader_form.is_valid()


def save_bundle(bundle: ReaderEditBundle, request) -> None:
    with transaction.atomic():
        user = bundle.user_form.save()
        if bundle.user_form.password_will_change():
            try:
                update_session_auth_hash(request, user)
            except Exception:
                pass

        bundle.reader_form.save()


def success_url() -> str:
    return reverse("home")


def add_validation_messages(request, bundle: ReaderEditBundle) -> None:
    if bundle.user_form.errors:
        for field, errors in bundle.user_form.errors.items():
            for error in errors:
                messages.error(request, f"{field.capitalize()}: {error}")
    elif bundle.reader_form.errors:
        for field, errors in bundle.reader_form.errors.items():
            for error in errors:
                messages.error(request, f"{field.capitalize()}: {error}")
    else:
        messages.error(request, "Erro ao atualizar os dados. Verifique os campos.")


def as_template_context(bundle: ReaderEditBundle) -> dict:
    return {
        "user_form": bundle.user_form,
        "reader_form": bundle.reader_form,
    }
