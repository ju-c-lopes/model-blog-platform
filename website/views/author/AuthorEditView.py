from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from website.services.author.author_profile_editor import (
    add_validation_messages,
    as_template_context,
    build_bundle,
    bundle_is_valid,
    can_edit,
    get_author_for_edit,
    save_bundle,
    success_url,
)

EDIT_AUTHOR_TEMPLATE = "blog/pages/edit-author/edit-author.html"


@login_required
def edit_author_profile(request, slug):
    author = get_author_for_edit(slug)

    if not can_edit(request.user, author):
        messages.error(request, "Você não tem permissão para editar este perfil.")
        return redirect("author", slug=slug)

    bundle = build_bundle(request, author)

    if request.method == "POST":
        if bundle_is_valid(bundle):
            save_bundle(bundle, request)
            messages.success(request, "Dados atualizados com sucesso.")
            return redirect(success_url(author))
        add_validation_messages(request, bundle)

    return render(request, EDIT_AUTHOR_TEMPLATE, as_template_context(bundle))


@login_required
def edit_author(request, author_slug=None):
    """Wrapper: sem slug usa o autor do usuário logado."""
    if not author_slug:
        author = getattr(request.user, "author", None)
        if not author:
            return redirect("/")
        slug = author.author_url_slug
    else:
        slug = author_slug
    return edit_author_profile(request, slug)
