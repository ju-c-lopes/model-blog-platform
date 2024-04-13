from django.urls import path
from website.views.SignUpView import sign_up_user

urlpatterns = [
    path("", sign_up_user, name='sign_up'),
]
