from django import forms

from website.models import SOCIAL_MEDIA
from website.models.author.AuthorSocialMediaModel import SocialMedia


class SocialMediaForm(forms.ModelForm):
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
