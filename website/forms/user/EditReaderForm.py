from django import forms

from website.models.user.ReaderModel import Reader


class EditReaderForm(forms.ModelForm):
    reader_name = forms.CharField(label="Nome completo", widget=forms.TextInput)
    image = forms.FileField(
        label="Foto do leitor", widget=forms.FileInput, required=False
    )

    class Meta:
        model = Reader
        fields = ["reader_name", "image"]
