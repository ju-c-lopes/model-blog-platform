from django.urls import path
from website.views.HomeView import get_home_page

urlpatterns = [
    path('', get_home_page, name='home'),
]
