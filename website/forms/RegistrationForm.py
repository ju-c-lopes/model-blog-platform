from website.forms import *
from website.models import Author, Reader, User
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm


class RegistrationAuthorForm(forms.ModelForm):

    author_name = forms.TextInput()
    
    class Meta:
        model = Author
        fields = ('author_name',)


class RegistrationReaderForm(forms.ModelForm):

    reader_name = forms.TextInput()
    
    class Meta:
        model = Reader
        fields = ('reader_name',)



class UserCreationForm(BaseUserCreationForm):
    
    phone = PhoneNumberField(
        label='Celular',
        region = 'BR',
    )

    class Meta:
        model = User
        fields = ("email", "phone_number",)
        
    password1 = forms.CharField(label='Senha:', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirme a senha:', widget=forms.PasswordInput, required=True)
    
    """def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2"""