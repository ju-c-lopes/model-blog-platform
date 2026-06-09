from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from website.models.author.AuthorModel import Author
from website.models.post.PostModel import Post
from website.services.post import post_content_images as images


@login_required
@require_POST
def upload_post_content_image(request):
    try:
        author = Author.objects.get(user=request.user)
    except Author.DoesNotExist:
        return JsonResponse({"error": "Perfil de autor necessário."}, status=403)

    uploaded_file = request.FILES.get("image")
    if not uploaded_file:
        return JsonResponse({"error": "Nenhuma imagem enviada."}, status=400)

    url_slug = request.POST.get("url_slug", "").strip()
    upload_session_id = request.POST.get("upload_session_id", "").strip()

    try:
        if url_slug:
            post = Post.objects.get(url_slug=url_slug)
            if post.author_id != author.id:
                return JsonResponse({"error": "Sem permissão para editar este post."}, status=403)
            image_url = images.save_content_image(uploaded_file, slug=url_slug)
        else:
            session_id = upload_session_id or request.session.get("post_content_upload_session")
            expected = request.session.get("post_content_upload_session")

            if upload_session_id and not expected:
                try:
                    images._validate_session_id(upload_session_id)
                    request.session["post_content_upload_session"] = upload_session_id
                    request.session.modified = True
                    session_id = upload_session_id
                except ValueError:
                    return JsonResponse({"error": "Sessão de upload inválida."}, status=400)
            elif expected and session_id != expected:
                return JsonResponse({"error": "Sessão de upload inválida."}, status=400)
            elif not session_id:
                return JsonResponse({"error": "Sessão de upload inválida."}, status=400)

            image_url = images.save_content_image(uploaded_file, session_id=session_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post não encontrado."}, status=404)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    return JsonResponse({"success": True, "url": image_url})
