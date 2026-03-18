from django.urls import path

# from website.views.author.AuthorView import edit_author_profile, view_author_page
from website.views.author.TeamView import view_team

urlpatterns = [
    path("", view_team, name="team"),
    # path("<str:slug>", view_author_page, name="author"),
    # path("<str:slug>/edit", edit_author_profile, name="edit_author"),
]
