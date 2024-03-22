from django import forms
from django.forms import ModelForm
from website.models import Author
from django.contrib.auth.models import User

class EditAuthorForm(ModelForm):

    class Meta:
        model = Author
        fields = ['author_name', 'image']

        widgets = {
            'author_name': forms.TextInput(),
            'image': forms.FileInput(),
        }

class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['username']
    
        username = forms.TextInput()