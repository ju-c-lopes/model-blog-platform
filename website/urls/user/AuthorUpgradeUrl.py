from django.urls import path

from website.views.user.AuthorUpgradeView import author_upgrade

urlpatterns = [
    path("", author_upgrade, name="author-upgrade"),
]
