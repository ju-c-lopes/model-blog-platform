from website.forms import *
from website.models import Author
from website.models import User
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm


class RegistrationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True)

    author_name = forms.TextInput()
    

    class Meta:
        model = Author
        fields = ('author_name',)
    

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2


class UserCreationForm(BaseUserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email")