from django import forms


class ProfileUpdateForm(forms.Form):
    PROFILE_CHOICES = [
        ("author", "Autor"),
        ("reader", "Leitor"),
    ]

    profile_type = forms.ChoiceField(
        choices=PROFILE_CHOICES, widget=forms.RadioSelect, label="Tipo de Perfil"
    )

    name = forms.CharField(
        max_length=100,
        label="Nome",
        widget=forms.TextInput(attrs={"placeholder": "Digite seu nome"}),
    )

    image = forms.ImageField(
        required=False,
        label="Foto do Perfil",
        widget=forms.FileInput(attrs={"accept": "image/*"}),
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if user:
            # Pre-populate form if user has existing profile
            if hasattr(user, "author"):
                self.fields["profile_type"].initial = "author"
                self.fields["name"].initial = user.author.author_name
                if user.author.image:
                    self.fields["image"].initial = user.author.image
            elif hasattr(user, "reader"):
                self.fields["profile_type"].initial = "reader"
                self.fields["name"].initial = user.reader.reader_name
                if user.reader.image:
                    self.fields["image"].initial = user.reader.image
