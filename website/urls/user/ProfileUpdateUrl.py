from django.urls import path

from website.views.user.ProfileUpdateView import update_profile

urlpatterns = [
    path("", update_profile, name="update-profile"),
]
