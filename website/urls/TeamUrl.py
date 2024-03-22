from django.urls import path
from website.views.AuthorView import view_author_page, edit_author_profile

urlpatterns = [
    #path('', view_team, name='team'),
    path('<str:slug>', view_author_page, name='author'),
    path('<str:slug>/edit', edit_author_profile, name='edit_author'),
]
