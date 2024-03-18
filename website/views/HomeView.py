from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from website.models import PostModel

def get_home_page(request):
    return render(request, 'home-page/homepage.html')