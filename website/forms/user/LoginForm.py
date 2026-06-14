from django import forms


class LoginForm(forms.Form):
    identifier = forms.CharField(label="Email ou usuário", widget=forms.TextInput)
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "input-type-pass"}),
        required=False,
    )

    def clean_identifier(self):
        return self.cleaned_data["identifier"].strip()
