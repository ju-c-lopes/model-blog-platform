from django import forms

from website.models.user.ReaderModel import Reader


class EditReaderForm(forms.ModelForm):
    reader_name = forms.CharField(
        label="Nome completo",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    image = forms.FileField(
        label="Foto do leitor",
        widget=forms.FileInput(attrs={"class": "form-control-file"}),
        required=False,
    )

    class Meta:
        model = Reader
        fields = ["reader_name", "image"]

    def save(self, commit=True):
        if self.instance.pk:
            old_reader = Reader.objects.get(pk=self.instance.pk)
            if "image" in self.changed_data and old_reader.image:
                old_reader.image.delete(save=False)
        return super().save(commit=commit)
