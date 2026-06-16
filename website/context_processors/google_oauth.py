from django.conf import settings


def google_oauth(request):
    client_id = getattr(settings, "GOOGLE_OAUTH_CLIENT_ID", "") or ""
    return {
        "GOOGLE_OAUTH_ENABLED": bool(client_id),
        "GOOGLE_OAUTH_CLIENT_ID": client_id,
    }
