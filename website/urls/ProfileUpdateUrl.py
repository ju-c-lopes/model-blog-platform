from django.urls import path
from website.views.ProfileUpdateView import update_profile

urlpatterns = [
    path('', update_profile, name='update-profile'),
]
