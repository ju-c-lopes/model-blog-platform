from django.shortcuts import render

from website.models.author.AuthorModel import Author


def view_team(request):
    # jobs omitido: o card usa current_job (.filter), que não usa cache do prefetch;
    # carregar todos os jobs aqui só aumentaria carga sem evitar N+1.
    authors = Author.objects.prefetch_related("graduations", "social_media").all()
    context = {
        "authors": authors,
    }
    return render(request, template_name="blog/pages/our-team/our-team.html", context=context)
