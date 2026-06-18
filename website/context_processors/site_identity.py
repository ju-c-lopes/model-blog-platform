from django.conf import settings


def site_identity(request):
    return {
        "SITE_BRAND_NAME": settings.SITE_BRAND_NAME,
        "SITE_CONTACT_EMAIL": settings.SITE_CONTACT_EMAIL,
        "SITE_LOCATION_CITY": settings.SITE_LOCATION_CITY,
        "SITE_LOCATION_STATE": settings.SITE_LOCATION_STATE,
        "SITE_RESPONSIBLE_NAME": settings.SITE_RESPONSIBLE_NAME,
    }
