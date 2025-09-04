from django.urls import path

from website.views.SearchView import search_posts

urlpatterns = [
    path("", search_posts, name="search_posts"),
]
