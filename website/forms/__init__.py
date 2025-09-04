from django import forms  # re-export used by submodule files (LoginForm)  # noqa: F401

from .EditAuthorForm import EditAuthorForm, SocialMediaForm, UserChangeForm
from .EditReaderForm import EditReaderForm
from .LoginForm import LoginForm
from .RegistrationForm import (
    RegistrationAuthorForm,
    RegistrationReaderForm,
    UserCreationForm,
)

# Explicit re-exports for package consumers
__all__ = [
    "EditAuthorForm",
    "SocialMediaForm",
    "UserChangeForm",
    "EditReaderForm",
    "LoginForm",
    "RegistrationAuthorForm",
    "RegistrationReaderForm",
    "UserCreationForm",
]
