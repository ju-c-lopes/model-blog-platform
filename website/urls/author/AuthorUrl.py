from django.urls import path

from website.views.author.AuthorView import view_author_page

urlpatterns = [
    path("<str:slug>", view_author_page, name="author"),
]
