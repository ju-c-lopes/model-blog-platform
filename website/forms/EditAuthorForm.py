from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.forms import ModelForm

from website.models import Author, SocialMedia
from website.models.__init__ import SOCIAL_MEDIA
from website.models.GraduationsModel import Graduation
from website.models.JobsModel import Job

User = get_user_model()


class EditAuthorForm(ModelForm):
    author_name = forms.CharField(
        label="Nome completo", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    image = forms.FileField(
        label="Foto do autor",
        widget=forms.FileInput(attrs={"class": "form-control-file"}),
        required=False,
    )

    class Meta:
        model = Author
        fields = ["author_name", "image"]


class UserChangeForm(BaseUserChangeForm):
    username = forms.CharField(
        label="Nome do Usuário", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Digite a nova senha", "class": "form-control"}
        ),
        required=False,
    )
    confirm_pass = forms.CharField(
        label="Confirme a senha",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Repita a nova senha", "class": "form-control"}
        ),
        required=False,
    )

    class Meta:
        model = User
        fields = ("username", "email", "password", "confirm_pass")

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
        pw = self.cleaned_data.get("password")
        if pw:
            user.set_password(pw)
        if commit:
            user.save()
        return user


class SocialMediaForm(ModelForm):
    social_media = forms.ChoiceField(
        choices=SOCIAL_MEDIA,
        widget=forms.Select(attrs={"class": "custom-select"}),
        required=False,
    )
    social_media_profile = forms.CharField(
        label="Perfil",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )

    class Meta:
        model = SocialMedia
        fields = ["social_media", "social_media_profile"]


class GraduationForm(ModelForm):
    class Meta:
        model = Graduation
        fields = [
            "graduation_level",
            "course",
            "school",
            "year_graduation",
            "concluded",
        ]
        widgets = {
            "graduation_level": forms.Select(attrs={"class": "custom-select"}),
            "course": forms.TextInput(attrs={"class": "form-control"}),
            "school": forms.TextInput(attrs={"class": "form-control"}),
            "year_graduation": forms.NumberInput(
                attrs={"class": "form-control", "min": 1900, "max": 2100}
            ),
            "concluded": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = [
            "occupation",
            "month_begin",
            "year_begin",
            "month_end",
            "year_end",
            "current_job",
            "roles_description",
        ]
        widgets = {
            "occupation": forms.TextInput(attrs={"class": "form-control"}),
            "month_begin": forms.Select(attrs={"class": "custom-select"}),
            "year_begin": forms.NumberInput(
                attrs={"class": "form-control", "min": 1900, "max": 2100}
            ),
            "month_end": forms.Select(attrs={"class": "custom-select"}),
            "year_end": forms.NumberInput(
                attrs={"class": "form-control", "min": 1900, "max": 2100}
            ),
            "current_job": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "roles_description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }
