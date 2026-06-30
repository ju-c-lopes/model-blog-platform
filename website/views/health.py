from django.http import JsonResponse

from website.services.health import HealthService


def health(request):
    result = HealthService.check()

    status = 200 if all(result.values()) else 500

    return JsonResponse(
        {
            "status": "ok" if status == 200 else "error",
            **result,
        },
        status=status,
    )
