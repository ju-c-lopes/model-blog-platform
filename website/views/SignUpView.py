from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from website.models import User
from website.models import Author
from django.contrib import messages
from django.contrib.messages import get_messages

def sign_up(request):
    
    context = {}
    #context.add("user", )
    return render(request, template_name="sign-up/sign-up.html", status=200)