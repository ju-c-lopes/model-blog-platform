from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from phonenumber_field.formfields import PhoneNumberField

from website.models.user.UserModel import User


class UserCreationForm(BaseUserCreationForm):
    phone = PhoneNumberField(
        label="Celular",
        region="BR",
    )

    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
        )

    password1 = forms.CharField(label="Senha:", widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label="Confirme a senha:", widget=forms.PasswordInput, required=True)
