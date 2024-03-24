from django import forms
from django.forms import ModelForm
from website.models import Author, SocialMedia
from website.models.__init__ import SOCIAL_MEDIA
from django.contrib.auth.models import User

class EditAuthorForm(ModelForm):

    author_name = forms.CharField(label='Nome completo', widget=forms.TextInput)
    image = forms.FileField(label='Foto do autor', widget=forms.FileInput, required=False)
    
    class Meta:
        model = Author
        fields = ['author_name', 'image']

        # widgets = {
        #     'author_name': forms.TextInput(label='Nome completo'),
        #     'image': forms.FileInput(label='Foto do author'),
        # }

class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['username']
    
        username = forms.CharField(label='Nome do Usuário', widget=forms.TextInput)

class SocialMediaForm(ModelForm):

    social_media = forms.ChoiceField(
        choices=SOCIAL_MEDIA,
        widget=forms.Select,
    )
    social_media_profile = forms.CharField(label='Perfil', widget=forms.TextInput)

    class Meta:
        model = SocialMedia
        fields = ['social_media', 'social_media_profile']