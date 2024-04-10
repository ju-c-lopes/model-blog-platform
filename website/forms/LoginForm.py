from website.forms import *

class LoginForm(forms.Form):
    email = forms.CharField(label='Email', widget=forms.EmailInput)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput, required=False)