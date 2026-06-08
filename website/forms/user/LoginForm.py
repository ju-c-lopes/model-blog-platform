from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(label="Email", widget=forms.EmailInput)
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "input-type-pass"}),
        required=False,
    )
