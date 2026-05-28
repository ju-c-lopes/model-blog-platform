from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm

User = get_user_model()


class UserChangeForm(BaseUserChangeForm):
    username = forms.CharField(label="Nome do Usuário", widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"placeholder": "Digite a nova senha", "class": "form-control"}),
        required=False,
    )
    confirm_pass = forms.CharField(
        label="Confirme a senha",
        widget=forms.PasswordInput(attrs={"placeholder": "Repita a nova senha", "class": "form-control"}),
        required=False,
    )

    class Meta:
        model = User
        # password/confirm_pass são campos de UI — não mapear direto ao model
        fields = ("username", "email")

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get("password")
        cpw = cleaned.get("confirm_pass")
        if pw or cpw:
            if pw != cpw:
                self.add_error("confirm_pass", "As senhas não coincidem.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

    def password_will_change(self) -> bool:
        if not hasattr(self, "cleaned_data"):
            return False
        return bool(self.cleaned_data.get("password"))
