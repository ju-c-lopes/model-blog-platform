from django.urls import path

from website.views.user.SignUpView import sign_up_user

urlpatterns = [
    path("", sign_up_user, name="sign_up"),
]
