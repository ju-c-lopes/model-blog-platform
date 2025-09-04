from django.http import Http404
from django.shortcuts import render


class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # If the response status code is 404, render our custom 404 page
        if response.status_code == 404:
            return render(request, "errors/404.html", status=404)

        return response

    def process_exception(self, request, exception):
        # Handle 404 exceptions
        if isinstance(exception, Http404):
            return render(request, "errors/404.html", status=404)

        # For other exceptions, return None to let Django handle it
        return None
