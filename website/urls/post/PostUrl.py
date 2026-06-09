from django.urls import path

from website.views.post.PostContentImageUploadView import upload_post_content_image
from website.views.post.PostCreateView import edit_post
from website.views.post.PostView import post_detail, toggle_like, toggle_love

urlpatterns = [
    path("create/", edit_post, name="create_post"),
    path("upload-content-image/", upload_post_content_image, name="post_upload_content_image"),
    path("edit/<str:url_slug>/", edit_post, name="edit_post"),
    path("<str:url_slug>/", post_detail, name="post_detail"),
    path("<str:url_slug>/like/", toggle_like, name="post_toggle_like"),
    path("<str:url_slug>/love/", toggle_love, name="post_toggle_love"),
]
