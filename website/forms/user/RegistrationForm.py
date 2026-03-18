from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

from website.models.author.AuthorModel import Author
from website.models.user.ReaderModel import Reader
from website.models.user.UserModel import User


class RegistrationAuthorForm(forms.ModelForm):
    author_name = forms.TextInput()

    class Meta:
        model = Author
        fields = ("author_name",)


class RegistrationReaderForm(forms.ModelForm):
    image = forms.FileField(
        label="Foto do perfil",
        widget=forms.FileInput(attrs={"class": "form-control-file"}),
        required=False,
    )

    class Meta:
        model = Reader
        fields = ("image",)
