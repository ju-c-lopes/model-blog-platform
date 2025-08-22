from django.urls import path
from website.views.PostView import post_detail
from website.views.PostCreateView import create_post, edit_post

urlpatterns = [
    path('create/', create_post, name='create_post'),
    path('edit/<str:url_slug>/', edit_post, name='edit_post'),
    path('<str:url_slug>/', post_detail, name='post_detail'),
]