from django import forms
from django.contrib.auth import get_user_model

from website.models import SOCIAL_MEDIA
from website.models.author.AuthorModel import Author

User = get_user_model()


class EditAuthorForm(forms.ModelForm):
    author_name = forms.CharField(
        label="Nome completo", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    gender = forms.ChoiceField(
        label="Gênero",
        choices=(("M", "Masculino"), ("F", "Feminino")),
        widget=forms.Select(attrs={"class": "custom-select"}),
    )
    image = forms.FileField(
        label="Foto do autor",
        widget=forms.FileInput(attrs={"class": "form-control-file"}),
        required=False,
    )

    class Meta:
        model = Author
        fields = ["author_name", "gender", "image"]
