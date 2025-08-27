from django.urls import path

from website.views.PostCreateView import edit_post
from website.views.PostView import post_detail

urlpatterns = [
    path("create/", edit_post, name="create_post"),
    path("edit/<str:url_slug>/", edit_post, name="edit_post"),
    path("<str:url_slug>/", post_detail, name="post_detail"),
]
