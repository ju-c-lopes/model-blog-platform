from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from website.models.author.AuthorModel import Author
from website.services.user.admin_approval import verify_superuser_credentials
from website.services.user.user_registration import create_author_profile


@login_required
def author_upgrade(request):
    if Author.objects.filter(user=request.user).exists():
        messages.info(request, "Você já possui perfil de autor.")
        return redirect("reader-edit")

    reader = getattr(request.user, "reader", None)
    if reader is None or not reader.author_upgrade_invited:
        messages.error(request, "Você não possui convite para solicitar perfil de autor.")
        return redirect("reader-edit")

    reader_name = reader.reader_name or ""

    if request.method == "GET":
        return render(
            request,
            "blog/pages/user/author-upgrade.html",
            {"author_name": reader_name, "aprovar": False},
        )

    author_name = (request.POST.get("author_name") or reader_name or request.user.username).strip()
    is_approval_step = request.POST.get("approval") == "1"

    if is_approval_step:
        if not verify_superuser_credentials(
            request.POST.get("super", ""),
            request.POST.get("pass-super", ""),
        ):
            messages.error(request, "Credenciais de administrador inválidas.")
            return render(
                request,
                "blog/pages/user/author-upgrade.html",
                {"author_name": author_name, "aprovar": True},
            )
        user = request.user
        user.is_staff = True
        user.save(update_fields=["is_staff"])
        create_author_profile(user, author_name)
        messages.success(request, "Perfil de autor criado com sucesso.")
        return redirect("home")

    if not author_name:
        messages.error(request, "Informe o nome para o perfil de autor.")
        return render(
            request,
            "blog/pages/user/author-upgrade.html",
            {"author_name": author_name, "aprovar": False},
        )

    return render(
        request,
        "blog/pages/user/author-upgrade.html",
        {"author_name": author_name, "aprovar": True},
    )
