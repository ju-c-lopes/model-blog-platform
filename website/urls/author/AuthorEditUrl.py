from django.urls import path

from website.views.author.AuthorEditView import edit_author_profile

urlpatterns = [
    path("<str:slug>/edit", edit_author_profile, name="edit_author"),
]
