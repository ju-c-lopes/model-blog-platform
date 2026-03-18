from django.urls import path

from website.views.user.LogoutView import logout_user

urlpatterns = [
    path("", logout_user, name="logout"),
]
