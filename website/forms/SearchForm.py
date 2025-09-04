from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search for posts...",
                "aria-label": "Search",
            }
        ),
    )
