from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render

from website.services.reader.reader_profile_editor import (
    add_validation_messages,
    as_template_context,
    build_bundle,
    bundle_is_valid,
    can_edit,
    get_reader_for_edit,
    save_bundle,
    success_url,
)

EDIT_READER_TEMPLATE = "blog/pages/edit-reader/edit-reader.html"


@login_required
def reader_edit(request):
    try:
        reader = get_reader_for_edit(request.user)
    except Http404:
        messages.error(request, "Perfil de leitor não encontrado.")
        return redirect("home")

    if not can_edit(request.user, reader):
        messages.error(request, "Você não tem permissão para editar este perfil.")
        return redirect("home")

    bundle = build_bundle(request, reader)

    if request.method == "POST":
        if bundle_is_valid(bundle):
            save_bundle(bundle, request)
            messages.success(request, "Dados atualizados com sucesso.")
            return redirect(success_url())
        add_validation_messages(request, bundle)

    return render(request, EDIT_READER_TEMPLATE, as_template_context(bundle))
