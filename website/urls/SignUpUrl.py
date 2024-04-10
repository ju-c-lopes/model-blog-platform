from django.urls import path
from website.views.SignUpView import sign_up

urlpatterns = [
    path("", sign_up, name='sign_up'),
]
