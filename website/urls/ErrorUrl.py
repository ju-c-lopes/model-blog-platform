from django.urls import path
from django.views.generic import TemplateView

# For testing error pages
urlpatterns = [
    path('404/', TemplateView.as_view(template_name='errors/404.html'), name='test_404'),
    path('500/', TemplateView.as_view(template_name='errors/500.html'), name='test_500'),
    path('403/', TemplateView.as_view(template_name='errors/403.html'), name='test_403'),
]