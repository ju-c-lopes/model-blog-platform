from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Buscar posts...",
                "aria-label": "Buscar posts",
            }
        ),
    )
