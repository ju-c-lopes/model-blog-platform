from django.urls import path

from website.views.author.AuthorEditView import edit_author_profile

# Montado em blogModel/urls.py sob prefixo nossa-equipe/
urlpatterns = [
    path("<str:slug>/edit", edit_author_profile, name="edit_author"),
]
