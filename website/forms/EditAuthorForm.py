from django import forms
from django.forms import ModelForm
from website.models import Author, SocialMedia
from website.models.__init__ import SOCIAL_MEDIA
from website.models import User
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm

class EditAuthorForm(ModelForm):

    author_name = forms.CharField(label='Nome completo', widget=forms.TextInput)
    image = forms.FileField(label='Foto do autor', widget=forms.FileInput, required=False)
    
    class Meta:
        model = Author
        fields = ['author_name', 'image']

class UserChangeForm(BaseUserChangeForm):
    username = forms.CharField(label='Nome do Usuário', widget=forms.TextInput)
    email = forms.EmailField(label="Email", widget=forms.EmailInput)
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={'placeholder': 'Digite a nova senha'}), required=False)
    confirm_pass = forms.CharField(label="Confirme a senha", widget=forms.PasswordInput(attrs={'placeholder': 'Repita a nova senha'}), required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password", "confirm_pass")
    

class SocialMediaForm(ModelForm):

    social_media = forms.ChoiceField(
        choices=SOCIAL_MEDIA,
        widget=forms.Select,
        required=False,
    )
    social_media_profile = forms.CharField(label='Perfil', widget=forms.TextInput, required=False)

    class Meta:
        model = SocialMedia
        fields = ['social_media', 'social_media_profile']