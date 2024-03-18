from django.urls import path
from website.views.AuthorView import view_author_page

urlpatterns = [
    #path('', view_team, name='team'),
    path('<str:slug>', view_author_page, name='author'),
]
