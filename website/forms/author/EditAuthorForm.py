from django import forms
from django.contrib.auth import get_user_model

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

    def save(self, commit=True):
        if self.instance.pk:
            old_author = Author.objects.get(pk=self.instance.pk)
            # If a new image is being uploaded and an old one exists, delete the old one
            if "image" in self.changed_data and old_author.image:
                old_author.image.delete(save=False)
        return super().save(commit=commit)
