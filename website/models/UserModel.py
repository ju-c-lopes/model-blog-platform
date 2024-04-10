from django.db import models
from website.manager import UserManager
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    username = models.TextField(max_length=30, unique=True)
    email = models.EmailField("Email Address", unique=True)
    phone_number = PhoneNumberField(blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.username} => @:{self.email}"
